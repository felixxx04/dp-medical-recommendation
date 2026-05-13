"""
批量疾病推荐验证脚本
测试73种vocab疾病之外的疾病推荐准确性
"""
import requests
import json
import time
import sys

sys.path.insert(0, 'D:/grad_medical/medical-model')
from app.utils.disease_mapper import CHINESE_TO_ENGLISH_DISEASE

# 73种vocab疾病列表
VOCAB_DISEASES = {
    'acid reflux', 'acne', 'acute bacterial sinusitis', 'adenocarcinoma of pancreas',
    'allergic rhinitis', 'allergy', 'anemia', 'angina', 'anxiety', 'arrhythmia',
    'asthma', 'atopic dermatitis', 'back pain', 'bacterial conjunctivitis',
    'bacterial infections', 'bacterial skin infection', 'bacterial urinary tract infection',
    'benign prostatic hyperplasia', 'bipolar disorder', 'breast cancer',
    'chronic kidney disease', 'chronic pain', 'common cold', 'conjunctivitis',
    'deep vein thrombosis', 'depression', 'diabetes', 'diarrhea',
    'diverticulitis of gastrointestinal tract', 'eczema', 'edema', 'endometriosis',
    'epilepsy', 'erectile dysfunction', 'fever', 'fibromyalgia', 'flatulence',
    'gastroesophageal reflux disease', 'glaucoma', 'gout', 'headache', 'heart failure',
    'hemorrhoids', 'hiv', 'hiv infection', 'hypercholesterolemia', 'hypertension',
    'hyperthyroidism', 'insomnia', 'joint pain', 'migraine', 'nausea', 'nerve pain',
    'obesity', 'osteoarthritis', 'osteoporosis', 'otitis media', 'peptic ulcer',
    'pharyngitis due to streptococcus pyogenes', 'pneumonia',
    'prevention of cerebrovascular accident', 'psoriasis', 'rheumatoid arthritis',
    'rosacea', 'schizophrenia', 'seizures', 'sore throat', 'stomach pain',
    'tuberculosis', 'type 2 diabetes', 'urinary tract infection', 'vertigo',
    'vulvovaginal candidiasis',
}

def is_vocab_disease(en_list):
    """Check if any disease in the English list is in vocab"""
    for en in en_list:
        if en.lower() in VOCAB_DISEASES:
            return True
    return False

def test_disease(cn_name, en_list):
    """Test recommendation for a disease"""
    data = {
        'age': 55, 'gender': 'male', 'height': 170, 'weight': 65,
        'diseases': cn_name, 'allergies': '', 'medications': '',
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
        return {
            'cn': cn_name,
            'en': en_list,
            'drugs': drugs,
            'all_diseases': d.get('allDiseases', []),
            'in_vocab': is_vocab_disease(en_list),
        }
    except Exception as e:
        return {'cn': cn_name, 'en': en_list, 'error': str(e)}

# Test all diseases
results = []
for cn_name, en_list in CHINESE_TO_ENGLISH_DISEASE.items():
    result = test_disease(cn_name, en_list)
    results.append(result)
    status = 'OK' if 'drugs' in result else 'ERR'
    print(f'[{status}] {cn_name} ({en_list[0]}): {result.get("drugs", result.get("error", "?"))}')

# Save results
with open('verification_results/batch_disease_test.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Summary
vocab_count = sum(1 for r in results if r.get('in_vocab'))
non_vocab_count = sum(1 for r in results if not r.get('in_vocab'))
print(f'\nTotal tested: {len(results)}')
print(f'Vocab diseases: {vocab_count}')
print(f'Non-vocab (lost) diseases: {non_vocab_count}')