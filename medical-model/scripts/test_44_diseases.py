"""Test 44 non-vocab diseases for DeepSeek verification"""
import requests
import json
import sys

test_diseases = [
    '低血压', '冠心病', '心肌梗死', '房颤',
    '动脉粥样硬化', '肺栓塞', '高血脂',
    '1型糖尿病',
    '甲状腺功能减退', '甲减', '甲状腺肿', '代谢综合征',
    '慢阻肺', '支气管炎', '感冒',
    '胃溃疡', '胃炎', '肠炎',
    '溃疡性结肠炎', '克罗恩病', '肠易激综合征', '便秘',
    '肝炎', '胆囊炎', '胆结石',
    '尿路结石', '肾结石',
    '抑郁症', '焦虑症',
    '分簇性头痛', '帕金森病', '阿尔茨海默病', '老年痴呆',
    '多动症', '强迫症', '惊恐障碍', '社交焦虑',
    '脂肪肝', '肝硬化',
]

results = []
for cn in test_diseases:
    data = {
        'age': 55, 'gender': 'male', 'height': 170, 'weight': 65,
        'diseases': cn, 'allergies': '', 'medications': '',
        'renalFunction': 'normal', 'hepaticFunction': 'normal',
        'dpEnabled': False
    }
    try:
        r = requests.post('http://localhost:8001/model/predict', json=data, timeout=120)
        d = r.json()
        selected = d.get('selected', [])
        drugs = []
        for rec in selected:
            en = rec.get('englishName', '?')
            ev = rec.get('explanation', {}).get('evidenceLevel', '?')
            drugs.append(f'{en}({ev})')
        result = {'cn': cn, 'drugs': drugs}
        print(f'{cn}: {", ".join(drugs)}')
    except Exception as e:
        result = {'cn': cn, 'error': str(e)}
        print(f'{cn}: ERR {e}')
    results.append(result)

with open('verification_results/batch_44_diseases.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f'\nTotal tested: {len(results)}')
