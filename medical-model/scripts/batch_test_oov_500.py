"""Test out-of-vocab diseases via API + DeepSeek browser verification.

Strategy:
1. Load disease→drugs mapping (ground truth from pipeline_data)
2. Identify OOV diseases (not in model vocab)
3. Select 50 representative OOV diseases across medical categories
4. Call model API for each disease (as if patient has that disease)
5. Check if recommended drugs match ground truth
6. Save results for DeepSeek browser verification

API call format: POST /model/predict with patient data containing the disease.
"""

import json
import sys
import os
import time
import requests
from collections import defaultdict
from typing import Dict, List, Set, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

API_URL = "http://localhost:8001/model/predict"
BUDGET_RESET_URL = "http://localhost:8001/model/privacy/budget/reset"
REQUEST_COUNT = 0


def load_data():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'pipeline_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    encoder_path = os.path.join(os.path.dirname(__file__), '..', 'saved_models', 'encoder.json')
    with open(encoder_path, 'r', encoding='utf-8') as f:
        encoder = json.load(f)

    return data, encoder


def get_vocab_diseases(encoder: dict) -> set:
    vocab_maps = encoder.get('vocab_maps', {})
    pd = vocab_maps.get('primary_disease', {})
    return set(k.lower() for k in pd.keys() if k != '__unknown__')


def build_disease_to_drugs(data: dict) -> Dict[str, Set[str]]:
    mapping = defaultdict(set)
    for drug_name, drug_data in data.get('merged_drugs', {}).items():
        for ind in drug_data.get('indications', []) or []:
            cond = ind.get('condition', '') if isinstance(ind, dict) else str(ind)
            if cond:
                mapping[cond].add(drug_name)
    return dict(mapping)


def categorize_disease(disease: str) -> str:
    d = disease.lower()
    cats = {
        'cardiovascular': ['heart', 'cardiac', 'hypertension', 'angina', 'arrhythmia',
            'atrial', 'coronary', 'myocardial', 'thrombosis', 'embolism', 'vascular',
            'arterial', 'aortic', 'fibrillation', 'infarction', 'ischemic', 'stroke'],
        'respiratory': ['pulmonary', 'lung', 'bronch', 'pneumonia', 'asthma', 'copd',
            'respiratory', 'sinus', 'nasal', 'pharyng', 'tuberculosis', 'pneumothorax'],
        'endocrine': ['diabetes', 'thyroid', 'hyperthyroid', 'hypothyroid', 'adrenal',
            'pituitary', 'cushing', 'addison', 'obesity'],
        'gastrointestinal': ['gastric', 'stomach', 'intestin', 'colon', 'hepat',
            'liver', 'pancrea', 'esophag', 'duoden', 'cholecyst', 'diverticul',
            'crohn', 'colitis', 'diarrhea', 'constipation', 'gerd', 'reflux',
            'ulcer', 'hemorrhoid', 'bowel'],
        'neurological': ['seizure', 'epilepsy', 'migraine', 'headache', 'neuropathy',
            'neuralgia', 'multiple sclerosis', 'parkinson', 'alzheimer', 'dementia',
            'cerebr', 'brain', 'neuro', 'tremor'],
        'psychiatric': ['depression', 'anxiety', 'bipolar', 'schizo', 'psychosis',
            'panic', 'obsessive', 'compulsive', 'ptsd', 'adhd', 'insomnia'],
        'infectious': ['infection', 'bacterial', 'viral', 'fungal', 'parasitic',
            'hiv', 'hepatitis', 'influenza', 'covid', 'herpes', 'tuberculosis',
            'sepsis', 'meningitis'],
        'dermatological': ['dermatit', 'eczema', 'psoriasis', 'acne', 'rosacea',
            'urticaria', 'rash', 'skin', 'alopecia', 'cellulitis'],
        'musculoskeletal': ['arthritis', 'osteo', 'rheumatoid', 'gout', 'joint',
            'bone', 'muscle', 'fibromyalgia', 'back pain', 'spondyl', 'lupus'],
        'renal': ['kidney', 'renal', 'nephr', 'urinary', 'bladder', 'prostat',
            'cystitis', 'pyelonephritis', 'uti'],
        'oncological': ['cancer', 'carcinoma', 'tumor', 'neoplasm', 'leukemia',
            'lymphoma', 'melanoma', 'sarcoma', 'myeloma', 'adenocarcinoma'],
        'ophthalmological': ['eye', 'ocular', 'glaucoma', 'cataract', 'conjunctivitis',
            'retin', 'macular', 'optic', 'corneal'],
    }
    for cat, keywords in cats.items():
        if any(kw in d for kw in keywords):
            return cat
    return 'other'


def reset_privacy_budget():
    """Reset privacy budget to allow more API calls."""
    try:
        requests.post(BUDGET_RESET_URL + "?userId=default", timeout=5)
    except Exception:
        pass


def call_recommendation_api(disease: str, age: int = 55, gender: str = "male") -> dict:
    """Call the model API for a patient with a specific disease.

    Returns the full API response or None on failure.
    """
    # Build patient data matching the API format
    patient_data = {
        "age": age,
        "gender": gender,
        "weight": 70,
        "height": 170,
        "diseases": disease,  # English disease name as input
        "chronic_diseases": "",
        "allergies": "",
        "medications": "",
        "symptoms": "",
        "dpEnabled": False,  # Disable DP for testing (no budget limit)
    }

    try:
        resp = requests.post(API_URL, json=patient_data, timeout=120)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": f"HTTP {resp.status_code}", "body": resp.text[:200]}
    except Exception as e:
        return {"error": str(e)}


def select_test_diseases(
    disease_to_drugs: Dict[str, Set[str]],
    vocab_diseases: set,
    target: int = 50,
) -> List[str]:
    """Select target OOV diseases for testing, stratified by category."""
    eligible = {
        cond: drugs for cond, drugs in disease_to_drugs.items()
        if cond.lower() not in vocab_diseases and len(drugs) >= 3
    }

    by_cat = defaultdict(list)
    for cond in eligible:
        by_cat[categorize_disease(cond)].append(cond)

    # Sort each by drug count desc
    for cat in by_cat:
        by_cat[cat].sort(key=lambda c: len(eligible[c]), reverse=True)

    # Proportional allocation
    total_eligible = len(eligible)
    selected = []
    for cat, diseases in sorted(by_cat.items()):
        share = max(1, int(len(diseases) / total_eligible * target))
        selected.extend(diseases[:share])

    # Fill remaining
    if len(selected) < target:
        used = set(selected)
        remaining = sorted(
            [c for c in eligible if c not in used],
            key=lambda c: len(eligible[c]), reverse=True
        )
        selected.extend(remaining[:target - len(selected)])

    return selected[:target]


def check_recommendation_accuracy(
    api_result: dict,
    ground_truth_drugs: Set[str],
    disease: str,
) -> dict:
    """Check if API recommendations match ground truth.

    A drug is 'correct' if it appears in the ground truth set
    (i.e., it has an indication for this disease).
    """
    if 'error' in api_result:
        return {
            'apiSuccess': False,
            'error': api_result.get('error', 'unknown'),
        }

    selected = api_result.get('selected', [])
    if not selected:
        return {
            'apiSuccess': True,
            'recommendedCount': 0,
            'correctCount': 0,
            'accuracy': 0.0,
            'recommendedDrugs': [],
            'correctDrugs': [],
            'incorrectDrugs': [],
        }

    # Normalize drug names for comparison
    gt_lower = {d.lower() for d in ground_truth_drugs}

    recommended = []
    correct = []
    incorrect = []

    for rec in selected:
        drug_name = rec.get('englishName', rec.get('drugName', ''))
        recommended.append(drug_name)
        if drug_name.lower() in gt_lower:
            correct.append(drug_name)
        else:
            incorrect.append(drug_name)

    # Also check: how many ground truth drugs were found?
    gt_found = gt_lower & {d.lower() for d in recommended}
    gt_coverage = len(gt_found) / len(gt_lower) if gt_lower else 0

    return {
        'apiSuccess': True,
        'recommendedCount': len(recommended),
        'correctCount': len(correct),
        'accuracy': round(len(correct) / len(recommended), 3) if recommended else 0,
        'groundTruthCoverage': round(gt_coverage, 3),
        'recommendedDrugs': recommended,
        'correctDrugs': correct,
        'incorrectDrugs': incorrect,
        'matchedDisease': [rec.get('matchedDisease', '') for rec in selected],
        'scores': [rec.get('score', 0) for rec in selected],
    }


def main():
    print("Loading data...")
    data, encoder = load_data()
    vocab_diseases = get_vocab_diseases(encoder)
    disease_to_drugs = build_disease_to_drugs(data)

    print(f"Vocab diseases: {len(vocab_diseases)}")
    print(f"Total conditions: {len(disease_to_drugs)}")

    oov = {c: d for c, d in disease_to_drugs.items() if c.lower() not in vocab_diseases}
    oov_3plus = {c: d for c, d in oov.items() if len(d) >= 3}
    print(f"OOV conditions: {len(oov)}")
    print(f"OOV with >= 3 drugs: {len(oov_3plus)}")

    # Select 50 diseases for API testing
    print("\nSelecting 50 OOV diseases for API testing...")
    test_diseases = select_test_diseases(disease_to_drugs, vocab_diseases, target=50)
    print(f"Selected: {len(test_diseases)}")

    cat_dist = defaultdict(int)
    for d in test_diseases:
        cat_dist[categorize_disease(d)] += 1
    for cat, count in sorted(cat_dist.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    # Test each disease via API
    print("\nTesting diseases via API (this takes ~18s per request)...")
    results = []
    api_calls = 0

    for i, disease in enumerate(test_diseases):
        gt_drugs = disease_to_drugs.get(disease, set())
        print(f"\n[{i+1}/{len(test_diseases)}] {disease} ({len(gt_drugs)} drugs in ground truth)")

        # Reset privacy budget BEFORE each call (composition theorem burns budget fast)
        reset_privacy_budget()
        time.sleep(0.5)

        api_result = call_recommendation_api(disease)
        api_calls += 1

        # Also reset after to be safe
        reset_privacy_budget()

        accuracy = check_recommendation_accuracy(api_result, gt_drugs, disease)
        accuracy['disease'] = disease
        accuracy['category'] = categorize_disease(disease)
        accuracy['groundTruthDrugCount'] = len(gt_drugs)

        results.append(accuracy)

        if accuracy.get('apiSuccess'):
            print(f"  Recommended: {accuracy['recommendedCount']} drugs, "
                  f"Correct: {accuracy['correctCount']}, "
                  f"Accuracy: {accuracy['accuracy']:.1%}, "
                  f"GT Coverage: {accuracy.get('groundTruthCoverage', 0):.1%}")
            if accuracy.get('incorrectDrugs'):
                print(f"  Incorrect: {accuracy['incorrectDrugs'][:3]}")
        else:
            print(f"  API ERROR: {accuracy.get('error', 'unknown')}")

    # Calculate overall stats
    successful = [r for r in results if r.get('apiSuccess')]
    total = len(successful)
    if total:
        avg_accuracy = sum(r['accuracy'] for r in successful) / total
        avg_gt_coverage = sum(r.get('groundTruthCoverage', 0) for r in successful) / total
        perfect = sum(1 for r in successful if r['accuracy'] == 1.0)
        zero = sum(1 for r in successful if r['accuracy'] == 0.0)
    else:
        avg_accuracy = avg_gt_coverage = 0
        perfect = zero = 0

    print(f"\n{'='*60}")
    print(f"API TEST RESULTS — {total} OOV diseases")
    print(f"{'='*60}")
    print(f"  API success:    {total}/{len(results)}")
    print(f"  Avg accuracy:   {avg_accuracy:.1%}")
    print(f"  Avg GT coverage:{avg_gt_coverage:.1%}")
    print(f"  Perfect (100%): {perfect} ({perfect/total*100:.0f}%)")
    print(f"  Zero (0%):      {zero} ({zero/total*100:.0f}%)")

    # Per-category
    cat_results = defaultdict(list)
    for r in successful:
        cat_results[r['category']].append(r)

    print(f"\n  Per-category:")
    for cat in sorted(cat_results.keys()):
        cr = cat_results[cat]
        cat_acc = sum(r['accuracy'] for r in cr) / len(cr)
        cat_gt = sum(r.get('groundTruthCoverage', 0) for r in cr) / len(cr)
        print(f"    {cat:20s}: accuracy={cat_acc:.1%}, GT coverage={cat_gt:.1%}, n={len(cr)}")

    # Save results
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'verification_results_oov')
    os.makedirs(output_dir, exist_ok=True)

    # Full results
    output_path = os.path.join(output_dir, 'oov_api_50_results.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'totalTested': total,
                'apiSuccessCount': total,
                'avgAccuracy': round(avg_accuracy, 3),
                'avgGtCoverage': round(avg_gt_coverage, 3),
                'perfectCount': perfect,
                'zeroCount': zero,
                'categoryStats': {
                    cat: {
                        'count': len(cat_results[cat]),
                        'avgAccuracy': round(sum(r['accuracy'] for r in cat_results[cat]) / len(cat_results[cat]), 3),
                        'avgGtCoverage': round(sum(r.get('groundTruthCoverage', 0) for r in cat_results[cat]) / len(cat_results[cat]), 3),
                    }
                    for cat in sorted(cat_results.keys())
                },
            },
            'results': results,
        }, f, ensure_ascii=False, indent=2)
    print(f"\nResults saved to: {output_path}")

    # Prepare DeepSeek verification sample
    # Pick 20 diseases: 10 worst + 10 from different categories
    worst = sorted(successful, key=lambda r: r['accuracy'])[:10]
    by_cat_sample = []
    for cat in sorted(cat_results.keys()):
        if cat_results[cat]:
            by_cat_sample.append(cat_results[cat][0])
    by_cat_sample = by_cat_sample[:10]

    deepseek_verify = []
    for r in worst + by_cat_sample:
        deepseek_verify.append({
            'disease': r['disease'],
            'category': r['category'],
            'groundTruthDrugCount': r['groundTruthDrugCount'],
            'accuracy': r['accuracy'],
            'recommendedDrugs': r.get('recommendedDrugs', []),
            'correctDrugs': r.get('correctDrugs', []),
            'incorrectDrugs': r.get('incorrectDrugs', []),
        })

    ds_path = os.path.join(output_dir, 'deepseek_verify_20.json')
    with open(ds_path, 'w', encoding='utf-8') as f:
        json.dump(deepseek_verify, f, ensure_ascii=False, indent=2)
    print(f"DeepSeek sample saved to: {ds_path}")


if __name__ == '__main__':
    main()
