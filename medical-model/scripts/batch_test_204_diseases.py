"""Batch test 204 diseases and prepare results for DeepSeek verification."""
import requests
import json
import sys
import io
import time
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_URL = "http://localhost:8001/model/predict"
BUDGET_RESET_URL = "http://localhost:8001/model/privacy/budget/reset?userId=default"
OUTPUT_DIR = "verification_results_v2"
os.makedirs(OUTPUT_DIR, exist_ok=True)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.utils.disease_mapper import CHINESE_TO_ENGLISH_DISEASE

def reset_budget():
    try:
        requests.post(BUDGET_RESET_URL, timeout=10)
    except:
        pass

def test_disease(disease_cn):
    """Get recommendations for a single disease."""
    reset_budget()
    try:
        resp = requests.post(API_URL, json={
            'diseases': disease_cn,
            'age': 45,
            'gender': '男',
            'weight': 70,
            'height': 170,
            'allergies': '',
            'currentMedications': '',
            'dpEnabled': False,
            'topK': 10
        }, timeout=120)
        data = resp.json()
        recs = data.get('selected', [])
        result = {
            'disease_cn': disease_cn,
            'english_names': CHINESE_TO_ENGLISH_DISEASE.get(disease_cn, []),
            'recommendations': []
        }
        for r in recs:
            result['recommendations'].append({
                'englishName': r.get('englishName', ''),
                'drugName': r.get('drugName', ''),
                'category': r.get('category', ''),
                'score': r.get('score', 0),
                'rawScore': r.get('rawScore', 0),
                'matchedDisease': r.get('matchedDisease', ''),
                'safetyType': r.get('safetyType', ''),
            })
        return result
    except Exception as e:
        return {'disease_cn': disease_cn, 'error': str(e)}

def main():
    diseases = sorted(CHINESE_TO_ENGLISH_DISEASE.keys())
    print(f"Testing {len(diseases)} diseases...")

    all_results = []
    errors = 0

    for i, disease in enumerate(diseases):
        print(f"[{i+1}/{len(diseases)}] Testing: {disease}")
        result = test_disease(disease)
        if 'error' in result:
            print(f"  ERROR: {result['error']}")
            errors += 1
            # Reset service if needed
            time.sleep(2)
            reset_budget()
        else:
            rec_names = [r['englishName'] for r in result['recommendations'][:5]]
            print(f"  Top 5: {', '.join(rec_names)}")
        all_results.append(result)

        # Save intermediate results every 20 diseases
        if (i + 1) % 20 == 0:
            with open(os.path.join(OUTPUT_DIR, 'batch_results_partial.json'), 'w', encoding='utf-8') as f:
                json.dump(all_results, f, ensure_ascii=False, indent=2)
            print(f"  Saved partial results ({i+1} diseases)")

    # Save final results
    output_file = os.path.join(OUTPUT_DIR, 'batch_results_all.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Tested {len(diseases)} diseases, {errors} errors")
    print(f"Results saved to: {output_file}")

    # Generate DeepSeek verification prompts
    generate_verification_prompts(all_results)

def generate_verification_prompts(results):
    """Generate verification prompts for DeepSeek in batches of 30."""
    batch_size = 30
    batches = []

    for i in range(0, len(results), batch_size):
        batch = results[i:i+batch_size]
        prompt = "请评估以下用药推荐是否适当。对每种疾病，判断推荐的前5个药物是否适合治疗该疾病。\n\n"
        prompt += "评分标准:\n"
        prompt += "- APPROPRIATE: 推荐药物完全适合治疗该疾病\n"
        prompt += "- PARTIALLY: 部分推荐适合，部分不适合\n"
        prompt += "- INAPPROPRIATE: 推荐药物完全不适合\n\n"

        for r in batch:
            if 'error' in r:
                continue
            disease = r['disease_cn']
            en_names = ' / '.join(r['english_names'][:3])
            top5 = r['recommendations'][:5]
            drugs_str = '; '.join([
                f"{d['englishName']}({d['category']})" for d in top5
            ])
            prompt += f"疾病: {disease} ({en_names})\n推荐药物: {drugs_str}\n\n"

        prompt += "\n请对每种疾病给出评分(APPROPRIATE/PARTIALLY/INAPPROPRIATE)和简要理由。"

        batches.append(prompt)

    # Save prompts
    for i, prompt in enumerate(batches):
        prompt_file = os.path.join(OUTPUT_DIR, f'deepseek_prompt_batch_{i+1}.txt')
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)

    print(f"\nGenerated {len(batches)} DeepSeek verification prompts")
    print(f"Batch files: deepseek_prompt_batch_1.txt to deepseek_prompt_batch_{len(batches)}.txt")

if __name__ == '__main__':
    main()
