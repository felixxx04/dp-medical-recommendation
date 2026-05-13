"""Batch test all 204 diseases from disease_mapper against the recommendation system.
Outputs JSON results with top-8 drug recommendations per disease.
"""

import sys
import json
import time
import requests

# Get all diseases from disease_mapper
sys.path.insert(0, '.')
from app.utils.disease_mapper import CHINESE_TO_ENGLISH_DISEASE

all_diseases = sorted(CHINESE_TO_ENGLISH_DISEASE.keys())
print(f"Testing {len(all_diseases)} diseases...")

results = []
batch_size = 30
batch_num = 0

for i in range(0, len(all_diseases), batch_size):
    batch = all_diseases[i:i+batch_size]
    batch_num += 1

    # Reset budget before each batch
    try:
        requests.post("http://localhost:8001/model/privacy/budget/reset?userId=default", timeout=5)
    except:
        pass
    time.sleep(1)

    for disease in batch:
        try:
            resp = requests.post('http://localhost:8001/model/predict', json={
                'patient_id': 'batch_test',
                'diseases': disease,
                'age': 45,
                'gender': 'M',
                'renal_function': 'normal',
                'hepatic_function': 'normal',
            }, timeout=30)
            data = resp.json()
            selected = data.get('selected', [])
            english_names = [s.get('englishName', '') for s in selected[:8]]
            drug_names = [s.get('drugName', '') for s in selected[:8]]

            results.append({
                'disease': disease,
                'english_names': english_names,
                'drug_names': drug_names,
                'count': len(selected),
            })
            print(f"  {disease}: {len(selected)} recs - {english_names[:3]}")
            time.sleep(0.3)
        except Exception as e:
            results.append({
                'disease': disease,
                'english_names': [],
                'drug_names': [],
                'count': 0,
                'error': str(e),
            })
            print(f"  {disease}: ERROR - {e}")
            # Reset budget on error
            try:
                requests.post("http://localhost:8001/model/privacy/budget/reset?userId=default", timeout=5)
            except:
                pass
            time.sleep(2)

# Save results
output_file = f"verification_results_v2/batch_test_all_{len(all_diseases)}_diseases.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        'total_diseases': len(all_diseases),
        'total_results': len(results),
        'results': results,
    }, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(results)} results to {output_file}")
print(f"Diseases with 0 recs: {sum(1 for r in results if r['count'] == 0)}")
print(f"Diseases with >0 recs: {sum(1 for r in results if r['count'] > 0)}")