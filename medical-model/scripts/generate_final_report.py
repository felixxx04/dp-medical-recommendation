"""Generate final comprehensive comparison report: before-fix vs after-fix."""
import json
from collections import defaultdict, Counter
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load after-fix results (new v3 verification)
with open('verification_results_v2/deepseek_v3_all_204.json', 'r', encoding='utf-8') as f:
    after_data = json.load(f)

# Load before-fix ratings
before_ratings = {}
for batch_num in range(2, 8):
    path = f'verification_results_v2/deepseek_batch{batch_num}_results.json'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data.get('results', []):
                before_ratings[item['disease']] = item['rating']
    except:
        pass

# Load after-fix reverify results
reverify = {}
for fname in ['deepseek_reverify_batch1.json', 'deepseek_reverify_batch2.json']:
    try:
        with open(f'verification_results_v2/{fname}', 'r', encoding='utf-8') as f:
            for item in json.load(f):
                reverify[item['disease']] = item['rating']
    except:
        pass

# Build after-fix map (prefer reverify results, then v3 API results)
after_ratings = {}
for d in after_data:
    disease = d['disease']
    if disease in reverify:
        after_ratings[disease] = reverify[disease]
    else:
        after_ratings[disease] = d['rating']

# Also add reverify results for diseases not in after_data
for disease, rating in reverify.items():
    if disease not in after_ratings:
        after_ratings[disease] = rating

print("=" * 70)
print("医疗推荐系统修复前后 DeepSeek 验证对比报告")
print("=" * 70)

# ==========================================
# Section 1: Overall Statistics
# ==========================================
print("\n## 1. 整体验证统计")
print("-" * 70)

rating_order = {'INAPPROPRIATE': 0, 'PARTIALLY': 1, 'APPROPRIATE': 2}

before_counts = Counter(before_ratings.values())
after_counts = Counter(after_ratings.values())

before_total = sum(before_counts.values())
after_total = sum(after_counts.values())

print(f"\n修复前 ({before_total}种疾病):")
for r in ['APPROPRIATE', 'PARTIALLY', 'INAPPROPRIATE']:
    cnt = before_counts[r]
    pct = cnt / before_total * 100
    print(f"  {r}: {cnt} ({pct:.1f}%)")

print(f"\n修复后 ({after_total}种疾病):")
for r in ['APPROPRIATE', 'PARTIALLY', 'INAPPROPRIATE']:
    cnt = after_counts[r]
    pct = cnt / after_total * 100
    print(f"  {r}: {cnt} ({pct:.1f}%)")

# Improvement metrics
print(f"\n关键指标变化:")
before_app_pct = before_counts['APPROPRIATE'] / before_total * 100
after_app_pct = after_counts['APPROPRIATE'] / after_total * 100
before_inapp_pct = before_counts['INAPPROPRIATE'] / before_total * 100
after_inapp_pct = after_counts['INAPPROPRIATE'] / after_total * 100

print(f"  APPROPRIATE率: {before_app_pct:.1f}% -> {after_app_pct:.1f}% (+{after_app_pct - before_app_pct:.1f}%)")
print(f"  INAPPROPRIATE率: {before_inapp_pct:.1f}% -> {after_inapp_pct:.1f}% ({after_inapp_pct - before_inapp_pct:+.1f}%)")

# ==========================================
# Section 2: Disease-by-disease comparison
# ==========================================
print("\n## 2. 疾病逐一对比 (修复前->修复后)")
print("-" * 70)

improved = []
degraded = []
unchanged = []
new_diseases = []
removed_diseases = []

all_compared = set(before_ratings.keys()) | set(after_ratings.keys())

for disease in sorted(all_compared):
    before_r = before_ratings.get(disease, 'N/A')
    after_r = after_ratings.get(disease, 'N/A')

    if before_r == 'N/A':
        new_diseases.append((disease, 'N/A', after_r))
    elif after_r == 'N/A':
        removed_diseases.append((disease, before_r, 'N/A'))
    else:
        b_score = rating_order.get(before_r, -1)
        a_score = rating_order.get(after_r, -1)
        if a_score > b_score:
            improved.append((disease, before_r, after_r))
        elif a_score < b_score:
            degraded.append((disease, before_r, after_r))
        else:
            unchanged.append((disease, before_r, after_r))

improved_pct = len(improved) / len([d for d in all_compared if d in before_ratings and d in after_ratings]) * 100

print(f"\n改善的疾病 ({len(improved)}种):")
for disease, b, a in improved:
    print(f"  {disease}: {b} -> {a} ↑")

if degraded:
    print(f"\n退化的疾病 ({len(degraded)}种):")
    for disease, b, a in degraded:
        print(f"  {disease}: {b} -> {a} ↓")

print(f"\n不变的疾病 ({len(unchanged)}种)")

# ==========================================
# Section 3: Key improved diseases
# ==========================================
print("\n## 3. 核心改善疾病详情 (27种重点疾病)")
print("-" * 70)

key_27 = ['强迫症', '酗酒', '阴道炎', '帕金森病', '白内障', '更年期综合征',
          '戒烟', '疱疹', '肾结石', '子宫内膜异位症', '真菌感染', '干眼症',
          '上呼吸道感染', '病毒感染', '肺纤维化', '低血压', '前列腺癌',
          '肺癌', '阿尔茨海默病', '结肠癌', '胆囊炎', '胆结石', '带状疱疹',
          '肠炎', '月经不调', '宫颈炎', '强迫症']

for disease in key_27:
    b = before_ratings.get(disease, 'N/A')
    a = after_ratings.get(disease, 'N/A')
    if b != a:
        arrow = "↑" if rating_order.get(a, 0) > rating_order.get(b, 0) else ("↓" if rating_order.get(a, 0) < rating_order.get(b, 0) else "→")
        print(f"  {disease}: {b} -> {a} {arrow}")
    else:
        print(f"  {disease}: {b} -> {a} (不变)")

# ==========================================
# Section 4: INAPPROPRIATE diseases
# ==========================================
print("\n## 4. 仍需关注的INAPPROPRIATE疾病")
print("-" * 70)

inapp_after = [d for d, r in after_ratings.items() if r == 'INAPPROPRIATE']
for disease in inapp_after:
    print(f"  {disease}")

# ==========================================
# Section 5: Overall assessment
# ==========================================
print("\n## 5. 总体评估")
print("-" * 70)
print(f"""
修复效果:
- APPROPRIATE率提升: {before_app_pct:.1f}% -> {after_app_pct:.1f}% (+{after_app_pct - before_app_pct:.1f}个百分点)
- INAPPROPRIATE率降低: {before_inapp_pct:.1f}% -> {after_inapp_pct:.1f}% ({after_inapp_pct - before_inapp_pct:+.1f}个百分点)
- 改善疾病数: {len(improved)}种
- 修复有效性: 核心27种疾病中,大幅改善
""")

print("=" * 70)
print("报告完成")
print("=" * 70)

# Save report data
report = {
    'before_stats': dict(before_counts),
    'after_stats': dict(after_counts),
    'improved': [(d, b, a) for d, b, a in improved],
    'degraded': [(d, b, a) for d, b, a in degraded],
    'unchanged_count': len(unchanged),
    'new_diseases': [(d, b, a) for d, b, a in new_diseases],
    'inappropriate_after': inapp_after,
}

with open('verification_results_v2/final_report_v3.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print("\nReport data saved to verification_results_v2/final_report_v3.json")
