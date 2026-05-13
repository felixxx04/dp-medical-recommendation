"""快速50例推荐验证 — 修复版验证逻辑"""

import json
import sys
import time
import requests
import os
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPELINE_PATH = os.path.join(PROJECT_ROOT, "data", "pipeline_data.json")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "verification_results_post_fix")
os.makedirs(OUTPUT_DIR, exist_ok=True)

MODEL_URL = "http://localhost:8001"

with open(PIPELINE_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

all_patients = data['patient_records']
indication_map = data['indication_map']
merged_drugs = data['merged_drugs']

# Build drug indication lookup: drug_name_lower -> set of condition strings (lowercased)
drug_indication_lookup = {}
for drug_name, indications in indication_map.items():
    conditions = set()
    for ind in indications:
        cond = str(ind.get("condition", "")).lower()
        if cond:
            conditions.add(cond)
    drug_indication_lookup[drug_name.lower()] = conditions

# Also add from merged_drugs
for drug_name_key, drug_obj in merged_drugs.items():
    key = drug_name_key.lower()
    if key not in drug_indication_lookup:
        conditions = set()
        for ind in drug_obj.get("indications", []):
            cond = str(ind.get("condition", ind) if isinstance(ind, dict) else ind).lower()
            if cond:
                conditions.add(cond)
        drug_indication_lookup[key] = conditions

NUM_PATIENTS = 50
selected = all_patients[:NUM_PATIENTS]

def reset_budget():
    requests.post(f"{MODEL_URL}/model/privacy/budget/reset?userId=default", timeout=5)

reset_budget()

results = []
verifications = []

for i, patient in enumerate(selected):
    # Reset budget every 3 requests
    if i > 0 and i % 3 == 0:
        reset_budget()
        time.sleep(0.5)

    diseases = patient.get('diseases', []) + patient.get('chronic_diseases', [])
    disease_preview = ','.join(diseases[:3])
    print(f"[{i+1}/{NUM_PATIENTS}] 推荐患者 {patient.get('patient_id', '')} (疾病: {disease_preview}...)")

    request_data = {
        'diseases': ','.join(diseases),
        'age': patient.get('age', 55),
        'gender': patient.get('gender', 'male'),
        'topK': 4,
        'userId': 'default',
        'dpEnabled': True,
        'symptoms': '',
        'allergies': ','.join(patient.get('allergies', [])),
        'currentMedications': ','.join(patient.get('current_medications', [])),
        'renal_function': patient.get('renal_function', 'normal'),
        'hepatic_function': patient.get('hepatic_function', 'normal'),
    }

    try:
        start_time = time.time()
        resp = requests.post(f"{MODEL_URL}/model/predict", json=request_data, timeout=120)
        elapsed = time.time() - start_time
        if resp.status_code == 200:
            result = resp.json()
            print(f"  OK {elapsed:.1f}s, {len(result.get('selected', []))} recs")
        elif resp.status_code == 429 or 'PRIVACY_BUDGET' in resp.text:
            reset_budget()
            time.sleep(1)
            start_time = time.time()
            resp = requests.post(f"{MODEL_URL}/model/predict", json=request_data, timeout=120)
            elapsed = time.time() - start_time
            if resp.status_code == 200:
                result = resp.json()
                print(f"  Retry OK {elapsed:.1f}s")
            else:
                print(f"  Retry failed: {resp.status_code}")
                result = None
        else:
            print(f"  Failed: {resp.status_code}")
            result = None
    except Exception as e:
        print(f"  Error: {e}")
        result = None

    # Verify using indication_map
    patient_diseases = set(d.lower() for d in diseases)
    selected_drugs = result.get('selected', []) if result else []
    has_correct_match = False
    issues = []
    top_drugs = []

    for drug in selected_drugs[:5]:
        english_name = drug.get('englishName', '')
        drug_name_lower = english_name.lower()

        # Find drug indications from our lookup
        drug_conditions = drug_indication_lookup.get(drug_name_lower, set())

        # Check if any patient disease matches any drug indication
        indication_match = False
        matched_disease_names = []
        for pd in patient_diseases:
            for dc in drug_conditions:
                if pd in dc or dc in pd:
                    indication_match = True
                    matched_disease_names.append(dc)
                    break

        md = drug.get('matchedDisease', None)
        mc_list = drug.get('explanation', {}).get('indicationDetail', {}).get('matchedConditions', [])

        top_drugs.append({
            'drug': english_name,
            'matchedDisease': md,
            'matchedConditions': mc_list,
            'indicationMatch': indication_match,
            'matchedDiseasesFromData': matched_disease_names,
            'drugConditionsCount': len(drug_conditions),
        })

        if indication_match:
            has_correct_match = True

    if selected_drugs and not has_correct_match:
        issues.append('无一适应症匹配')
    for td in top_drugs:
        if td['matchedDisease'] and td['indicationMatch'] is False:
            issues.append(f"matchedDisease={td['matchedDisease']}但数据中不匹配")

    verification = {
        'patient_id': patient.get('patient_id', ''),
        'diseases': sorted(patient_diseases),
        'has_correct_match': has_correct_match,
        'total_selected': len(selected_drugs),
        'issues': issues,
        'top_drugs': top_drugs,
    }
    verifications.append(verification)
    results.append({'patient': patient, 'result': result, 'verification': verification})

# Summary
total = len(verifications)
api_success = sum(1 for v in verifications if v['total_selected'] > 0)
has_match = sum(1 for v in verifications if v['has_correct_match'])
no_match = sum(1 for v in verifications if v['total_selected'] > 0 and not v['has_correct_match'])
api_failed = total - api_success

print()
print("=" * 60)
print(f"验证报告 ({NUM_PATIENTS}例)")
print("=" * 60)
print(f"总患者数: {total}")
print(f"API成功: {api_success}/{total}")
print(f"API失败: {api_failed}/{total}")
match_rate = has_match / api_success * 100 if api_success > 0 else 0
print(f"适应症匹配正确: {has_match}/{api_success} ({match_rate:.1f}%)")
print(f"适应症不匹配: {no_match}/{api_success}")
print(f"有问题病例: {len([v for v in verifications if v['issues']])}")

# Show first 5 example matches
print("\n示例验证结果:")
for v in verifications[:5]:
    print(f"  患者{v['patient_id']} 疾病={v['diseases']} 匹配={v['has_correct_match']}")
    for td in v['top_drugs'][:3]:
        print(f"    药物={td['drug']} md={td['matchedDisease']} mc={td['matchedConditions']} match={td['indicationMatch']}")

# Disease accuracy
disease_acc = defaultdict(lambda: {'correct': 0, 'total': 0})
for v in verifications:
    for d in v['diseases']:
        disease_acc[d]['total'] += 1
        if v['has_correct_match']:
            disease_acc[d]['correct'] += 1

print("\n各疾病推荐正确率 (低于80%):")
for d, stats in sorted(disease_acc.items(), key=lambda x: x[1]['correct'] / max(x[1]['total'], 1)):
    if stats['total'] >= 2:
        rate = stats['correct'] / stats['total'] * 100
        marker = ' ⚠️' if rate < 80 else ''
        print(f"  {d}: {rate:.0f}% ({stats['correct']}/{stats['total']}){marker}")

# Save summary
summary = {
    'total_patients': total,
    'api_success_rate': api_success / total * 100,
    'indication_match_rate': match_rate,
    'error_cases': len([v for v in verifications if v['issues']]),
    'disease_accuracy': {
        d: f"{stats['correct']}/{stats['total']} ({stats['correct'] / stats['total'] * 100:.0f}%)"
        for d, stats in sorted(disease_acc.items()) if stats['total'] >= 2
    },
}
with open(os.path.join(OUTPUT_DIR, 'verification_summary.json'), 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print(f"\n验证摘要已保存: {OUTPUT_DIR}/verification_summary.json")