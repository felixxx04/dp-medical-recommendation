"""Re-test all 204 diseases after fixes using correct API format.
Uses model service direct API (not backend proxy) with proper epsilon."""
import json
import requests
import time
import re

DISEASE_MAPPER_PATH = "app/utils/disease_mapper.py"
OUTPUT_PATH = "verification_results_v2/retest_204_after_fix.json"
API_URL = "http://localhost:8001/model/predict"
BUDGET_RESET_URL = "http://localhost:8001/model/privacy/budget/reset"

def load_disease_names():
    with open(DISEASE_MAPPER_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'CHINESE_TO_ENGLISH_DISEASE.*?=\s*\{(.+?)\}', content, re.DOTALL)
    if not match:
        raise ValueError("Could not find CHINESE_TO_ENGLISH_DISEASE")
    dict_content = match.group(1)
    diseases = []
    for line in dict_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'"([^"]+)":\s*\[', line)
        if m:
            diseases.append(m.group(1))
    return diseases

def reset_budget():
    try:
        resp = requests.post(BUDGET_RESET_URL, params={"userId": "default"}, timeout=5)
        time.sleep(0.3)
    except Exception:
        pass

def get_recommendations(disease_cn, age=45, gender="male"):
    payload = {
        "patientId": 1,
        "age": age,
        "gender": gender,
        "diseases": disease_cn,
        "symptoms": "",
        "allergies": "",
        "currentMedications": "",
        "dpEnabled": True,
        "topK": 4,
        "dpConfig": {
            "epsilon": 1.0,
            "delta": 1e-5,
            "noiseMechanism": "laplace",
            "budget": 100
        },
        "userId": "default",
        "renal_function": "normal",
        "hepatic_function": "normal"
    }
    try:
        resp = requests.post(API_URL, json=payload, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            selected = data.get("selected", [])
            return selected
        elif resp.status_code == 429:
            print(f"  Budget exceeded for {disease_cn}, resetting...")
            reset_budget()
            time.sleep(1)
            resp = requests.post(API_URL, json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("selected", [])
            else:
                print(f"  Still failed after reset: {resp.status_code}")
                return []
        else:
            print(f"  Error {resp.status_code} for {disease_cn}")
            return []
    except Exception as e:
        print(f"  Exception for {disease_cn}: {e}")
        return []

def main():
    diseases = load_disease_names()
    print(f"Total diseases to test: {len(diseases)}")

    results = []
    reset_budget()

    for i, disease in enumerate(diseases):
        reset_budget()
        print(f"[{i+1}/{len(diseases)}] Testing {disease}...")
        recs = get_recommendations(disease)
        time.sleep(0.2)

        rec_data = []
        for r in recs:
            rec_data.append({
                "englishName": r.get("englishName", ""),
                "drugName": r.get("drugName", ""),
                "category": r.get("category", ""),
                "matchedDisease": r.get("matchedDisease", ""),
                "score": r.get("score", 0),
                "safetyType": r.get("safetyType", "")
            })

        results.append({
            "disease_cn": disease,
            "count": len(recs),
            "recommendations": rec_data
        })

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to {OUTPUT_PATH}")
    print(f"Total: {len(results)} diseases tested")

    has_recs = sum(1 for r in results if r["count"] > 0)
    no_recs = sum(1 for r in results if r["count"] == 0)
    print(f"With recommendations: {has_recs}")
    print(f"No recommendations: {no_recs}")

if __name__ == "__main__":
    main()