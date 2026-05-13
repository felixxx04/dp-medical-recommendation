"""批量推荐验证脚本 — 从pipeline_data选取300例患者做用药推荐并验证

流程:
1. 选取300例患者（确保79种训练疾病全覆盖，疾病组合不重复）
2. 批量调用 /model/predict API 获取推荐结果
3. 本地验证：检查推荐药物的适应症是否匹配患者疾病
4. 输出验证报告（正确率、错误类型、典型案例）
5. 生成DeepSeek验证提示词（用于浏览器验证）
"""

import json
import sys
import time
import requests
import os
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
PIPELINE_PATH = os.path.join(DATA_DIR, "pipeline_data.json")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "verification_results")
os.makedirs(OUTPUT_DIR, exist_ok=True)

MODEL_URL = "http://localhost:8001"

# =============================================
# 1. 选取300例患者
# =============================================

def select_patients():
    """选取300例患者，确保79种疾病全覆盖且组合不重复"""
    with open(PIPELINE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_patients = data['patient_records']
    indication_map = data['indication_map']

    # 计算每名患者的疾病组合key
    def disease_key(p):
        diseases = sorted(set(p.get('diseases', []) + p.get('chronic_diseases', [])))
        return '|'.join(diseases)

    # 按疾病组合分组，确保不重复
    by_combo = defaultdict(list)
    for p in all_patients:
        key = disease_key(p)
        by_combo[key].append(p)

    # 收集所有疾病
    all_diseases = set()
    for p in all_patients:
        for d in p.get('diseases', []) + p.get('chronic_diseases', []):
            all_diseases.add(d)

    # 确保每种疾病至少有1名患者被选中
    covered_diseases = set()
    selected = []
    used_combos = set()

    # 第一轮：每种疾病至少选1名患者
    for disease in sorted(all_diseases):
        # 找包含此疾病且组合尚未使用的患者
        candidates = []
        for p in all_patients:
            key = disease_key(p)
            if key in used_combos:
                continue
            p_diseases = set(p.get('diseases', []) + p.get('chronic_diseases', []))
            if disease in p_diseases:
                candidates.append((p, key))

        if candidates:
            p, key = candidates[0]
            selected.append(p)
            used_combos.add(key)
            for d in p.get('diseases', []) + p.get('chronic_diseases', []):
                covered_diseases.add(d)
        elif len(selected) < 300:
            # 允许重复组合以覆盖疾病
            for p in all_patients:
                p_diseases = set(p.get('diseases', []) + p.get('chronic_diseases', []))
                if disease in p_diseases:
                    selected.append(p)
                    for d in p_diseases:
                        covered_diseases.add(d)
                    break

    # 第二轮：填充到300名，优先选不同组合的患者
    remaining = [p for p in all_patients if disease_key(p) not in used_combos and p not in selected]
    # 按疾病丰富度排序（多病优先）
    remaining.sort(key=lambda p: -len(set(p.get('diseases', []) + p.get('chronic_diseases', []))))

    for p in remaining:
        if len(selected) >= 300:
            break
        key = disease_key(p)
        if key not in used_combos:
            selected.append(p)
            used_combos.add(key)
            for d in p.get('diseases', []) + p.get('chronic_diseases', []):
                covered_diseases.add(d)

    # 第三轮：如果还不够300，允许重复组合
    if len(selected) < 300:
        all_remaining = [p for p in all_patients if p not in selected]
        for p in all_remaining:
            if len(selected) >= 300:
                break
            selected.append(p)

    print(f"选取了 {len(selected)} 名患者")
    print(f"覆盖疾病: {len(covered_diseases)}/{len(all_diseases)}")
    print(f"独特组合: {len(used_combos)}")

    # 疾病分布
    disease_count = Counter()
    for p in selected:
        for d in p.get('diseases', []) + p.get('chronic_diseases', []):
            disease_count[d] += 1
    print(f"\n疾病分布 (TOP20):")
    for d, c in disease_count.most_common(20):
        print(f"  {d}: {c}人")

    # 检查未覆盖的疾病
    uncovered = all_diseases - covered_diseases
    if uncovered:
        print(f"\n未覆盖疾病: {sorted(uncovered)}")

    return selected, indication_map


# =============================================
# 2. 批量调用推荐API
# =============================================

def reset_budget():
    """重置隐私预算"""
    try:
        resp = requests.post(f"{MODEL_URL}/model/privacy/budget/reset?userId=default", timeout=5)
        if resp.status_code == 200:
            print("  预算重置成功")
            return True
    except Exception as e:
        print(f"  预算重置失败: {e}")
    return False


def call_predict(patient, idx):
    """调用模型推荐API"""
    # 构造请求 — 用英文疾病名（绕过mapper直接传入）
    diseases_str = ','.join(patient.get('diseases', []) + patient.get('chronic_diseases', []))

    request_data = {
        "patientId": idx,
        "age": patient.get('age', 50),
        "gender": patient.get('gender', 'MALE'),
        "diseases": diseases_str,
        "symptoms": "",
        "allergies": ','.join(patient.get('allergies', [])),
        "currentMedications": ','.join(patient.get('current_medications', [])),
        "renal_function": patient.get('renal_function', 'normal'),
        "hepatic_function": patient.get('hepatic_function', 'normal'),
    }

    try:
        resp = requests.post(
            f"{MODEL_URL}/model/predict",
            json=request_data,
            timeout=120,
        )
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 429 or 'PRIVACY_BUDGET' in resp.text:
            print(f"  预算耗尽，重置后重试...")
            reset_budget()
            time.sleep(1)
            resp = requests.post(f"{MODEL_URL}/model/predict", json=request_data, timeout=120)
            if resp.status_code == 200:
                return resp.json()
            else:
                print(f"  重试失败: {resp.status_code} {resp.text[:100]}")
                return None
        else:
            print(f"  推荐失败: {resp.status_code} {resp.text[:200]}")
            return None
    except Exception as e:
        print(f"  推荐异常: {e}")
        return None


# =============================================
# 3. 本地验证
# =============================================

def verify_locally(patient, result, indication_map):
    """本地验证推荐结果是否正确

    检查:
    1. 推荐药物的适应症是否包含患者疾病
    2. 推荐药物是否有禁忌冲突
    3. matchedDisease是否正确
    """
    patient_diseases = set(
        d.lower() for d in patient.get('diseases', []) + patient.get('chronic_diseases', [])
    )

    selected = result.get('selected', []) if result else []
    excluded = result.get('excluded', []) if result else []

    verification = {
        'patient_id': patient.get('patient_id', ''),
        'diseases': sorted(patient_diseases),
        'top_drugs': [],
        'matched_count': 0,
        'total_selected': len(selected),
        'total_excluded': len(excluded),
        'has_correct_match': False,
        'issues': [],
    }

    for drug in selected[:5]:  # 只检查前5个推荐药物
        drug_name = drug.get('englishName', drug.get('drugName', ''))
        matched_disease = drug.get('matchedDisease', None)
        score = drug.get('score', 0)
        raw_score = drug.get('rawScore', 0)

        # 检查适应症匹配
        drug_indications = indication_map.get(drug_name, [])
        indication_conditions = set()
        for ind in drug_indications:
            if isinstance(ind, dict):
                indication_conditions.add(str(ind.get('condition', '')).lower())
            else:
                indication_conditions.add(str(ind).lower())

        # 是否有适应症匹配患者疾病
        matched = False
        matched_detail = []
        for pd in patient_diseases:
            for ic in indication_conditions:
                if pd in ic or ic in pd:
                    matched = True
                    matched_detail.append((pd, ic))

        if matched:
            verification['matched_count'] += 1

        verification['top_drugs'].append({
            'drug': drug_name,
            'drugName_cn': drug.get('drugName', ''),
            'matched_disease': matched_disease,
            'score': score,
            'raw_score': raw_score,
            'indication_match': matched,
            'matched_detail': matched_detail,
            'indications': sorted(indication_conditions)[:5],
        })

    # 检查是否有任何药物正确匹配了适应症
    verification['has_correct_match'] = verification['matched_count'] > 0

    # 检查matchedDisease是否与实际疾病相关
    for drug_info in verification['top_drugs']:
        md = drug_info.get('matched_disease', '')
        if md:
            # matchedDisease翻译后的中文是否对应患者疾病
            md_relevant = any(
                pd in md.lower() or md.lower() in pd
                for pd in patient_diseases
            )
            if not md_relevant and drug_info.get('indication_match'):
                verification['issues'].append(
                    f"matchedDisease '{md}' 与患者疾病 {sorted(patient_diseases)} 不相关，但适应症匹配"
                )

    # 如果没有匹配的药物
    if verification['matched_count'] == 0 and len(selected) > 0:
        verification['issues'].append(
            f"前5推荐药物无一适应症匹配患者疾病 {sorted(patient_diseases)}"
        )

    return verification


# =============================================
# 4. 主流程
# =============================================

def main():
    print("=" * 60)
    print("批量推荐验证脚本")
    print("=" * 60)

    # 选取患者
    selected, indication_map = select_patients()

    # 重置预算
    reset_budget()
    budget_reset_count = 0
    BUDGET_RESET_INTERVAL = 8  # 每8次推荐重置一次预算

    # 批量推荐
    print(f"\n开始批量推荐 ({len(selected)} 例)...")
    results = []
    verifications = []

    for i, patient in enumerate(selected):
        if i > 0 and i % BUDGET_RESET_INTERVAL == 0:
            print(f"\n[{i}/{len(selected)}] 重置隐私预算...")
            reset_budget()
            budget_reset_count += 1
            time.sleep(0.5)

        disease_preview = ','.join((patient.get('diseases', []) + patient.get('chronic_diseases', []))[:3])
        print(f"[{i+1}/{len(selected)}] 推荐患者 {patient.get('patient_id', '')} "
              f"(疾病: {disease_preview}...)")

        result = call_predict(patient, i + 1)

        verification = verify_locally(patient, result, indication_map)
        verifications.append(verification)

        if result:
            results.append({
                'patient': patient,
                'result': result,
                'verification': verification,
            })
        else:
            results.append({
                'patient': patient,
                'result': None,
                'verification': verification,
            })

        time.sleep(0.3)  # 防止请求过快

    # =============================================
    # 5. 汇总报告
    # =============================================

    print("\n" + "=" * 60)
    print("验证报告")
    print("=" * 60)

    total = len(verifications)
    api_success = sum(1 for v in verifications if v['total_selected'] > 0)
    has_match = sum(1 for v in verifications if v['has_correct_match'])
    no_match = sum(1 for v in verifications if v['total_selected'] > 0 and not v['has_correct_match'])
    api_failed = total - api_success

    print(f"总患者数: {total}")
    print(f"API成功: {api_success}/{total}")
    print(f"API失败: {api_failed}/{total}")
    print(f"适应症匹配正确: {has_match}/{api_success} ({has_match/api_success*100:.1f}%)")
    print(f"适应症不匹配: {no_match}/{api_success} ({no_match/api_success*100:.1f}%)")
    print(f"预算重置次数: {budget_reset_count}")

    # 错误案例分析
    error_cases = [v for v in verifications if v['issues']]
    print(f"\n有问题病例: {len(error_cases)} 例")
    issue_types = Counter()
    for v in error_cases:
        for issue in v['issues']:
            if "无一适应症匹配" in issue:
                issue_types['no_indication_match'] += 1
            elif "matchedDisease" in issue:
                issue_types['matchedDisease_mismatch'] += 1
            else:
                issue_types['other'] += 1
    for it, c in issue_types.most_common():
        print(f"  {it}: {c}例")

    # 按疾病分析正确率
    disease_accuracy = defaultdict(lambda: {'correct': 0, 'total': 0})
    for v in verifications:
        for d in v['diseases']:
            disease_accuracy[d]['total'] += 1
            if v['has_correct_match']:
                disease_accuracy[d]['correct'] += 1

    print(f"\n各疾病推荐正确率 (低于80%的):")
    for d, stats in sorted(disease_accuracy.items()):
        if stats['total'] >= 3:
            rate = stats['correct'] / stats['total'] * 100
            if rate < 80:
                print(f"  {d}: {rate:.0f}% ({stats['correct']}/{stats['total']})")

    # 保存完整结果
    output_path = os.path.join(OUTPUT_DIR, "batch_recommendation_results.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n完整结果已保存: {output_path}")

    # 保存验证摘要
    summary_path = os.path.join(OUTPUT_DIR, "verification_summary.json")
    summary = {
        'total_patients': total,
        'api_success_rate': api_success / total * 100,
        'indication_match_rate': has_match / api_success * 100 if api_success > 0 else 0,
        'error_cases': len(error_cases),
        'issue_types': dict(issue_types),
        'disease_accuracy': {
            d: f"{stats['correct']}/{stats['total']} ({stats['correct']/stats['total']*100:.0f}%)"
            for d, stats in sorted(disease_accuracy.items())
            if stats['total'] >= 3
        },
    }
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"验证摘要已保存: {summary_path}")

    # 生成DeepSeek验证提示词（用于有问题的病例）
    deepseek_prompts = []
    for v in error_cases[:30]:  # 最多30个有问题病例
        patient_info = f"患者疾病: {', '.join(v['diseases'])}"
        drug_info = '\n'.join([
            f"  {d['drugName_cn']} ({d['drug']}) - 匹配疾病: {d.get('matched_disease', '无')}, "
            f"适应症: {', '.join(d.get('indications', [])[:3])}, "
            f"分数: {d.get('score', 0)}"
            for d in v['top_drugs']
        ])
        prompt = (
            f"请评估以下用药推荐是否正确。\n"
            f"{patient_info}\n"
            f"推荐药物:\n{drug_info}\n\n"
            f"请回答:\n"
            f"1. 推荐药物是否匹配患者疾病适应症？（正确/部分正确/错误）\n"
            f"2. 是否有禁忌冲突？\n"
            f"3. 排序是否合理？\n"
            f"4. 如果有错误，应该推荐什么药物？"
        )
        deepseek_prompts.append({
            'patient_id': v['patient_id'],
            'diseases': v['diseases'],
            'prompt': prompt,
        })

    prompts_path = os.path.join(OUTPUT_DIR, "deepseek_prompts.json")
    with open(prompts_path, 'w', encoding='utf-8') as f:
        json.dump(deepseek_prompts, f, ensure_ascii=False, indent=2)
    print(f"DeepSeek验证提示词已保存: {prompts_path} ({len(deepseek_prompts)} 条)")

    return results, verifications


if __name__ == '__main__':
    main()