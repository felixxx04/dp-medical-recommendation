"""Verify disease recommendations via DeepSeek API (Anthropic-compatible endpoint).
Processes all 204 diseases in batches, extracting APPROPRIATE/PARTIALLY/INAPPROPRIATE ratings."""
import json
import time
import re
import os
import sys
import io
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "https://api.deepseek.com/anthropic/v1/messages"
AUTH_TOKEN = os.environ.get('ANTHROPIC_AUTH_TOKEN', '')
MODEL = "deepseek-v4-pro"

RETEST_DATA = "verification_results_v2/retest_204_after_fix_v3.json"
OUTPUT_DIR = "verification_results_v2"
BATCH_SIZE = 15

def load_data():
    with open(RETEST_DATA, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_batches(data):
    batches = []
    current = []
    for d in data:
        disease = d['disease_cn']
        recs = d['recommendations'][:4]
        rec_lines = []
        for j, r in enumerate(recs):
            rec_lines.append(f'{j+1}. {r["englishName"]} ({r["category"]})')
        entry = f'{disease}: ' + '; '.join(rec_lines)
        current.append((disease, entry))
        if len(current) >= BATCH_SIZE:
            batches.append(current)
            current = []
    if current:
        batches.append(current)
    return batches

def call_api(prompt):
    payload = {
        'model': MODEL,
        'max_tokens': 2000,
        'messages': [{'role': 'user', 'content': prompt}]
    }
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': AUTH_TOKEN,
        'anthropic-version': '2023-06-01'
    }
    r = requests.post(BASE_URL, json=payload, headers=headers, timeout=120)
    if r.status_code == 200:
        data = r.json()
        for block in data.get('content', []):
            if block.get('type') == 'text':
                return block.get('text', '')
        return ''
    else:
        raise Exception(f"API error {r.status_code}: {r.text[:200]}")

def parse_ratings(text, expected_diseases):
    results = {}
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        for rating in ['APPROPRIATE', 'PARTIALLY', 'INAPPROPRIATE']:
            if rating in line:
                # Try to match the disease from expected list
                for disease in expected_diseases:
                    if disease in line:
                        results[disease] = rating
                        break
                break
    return results

def main():
    if not AUTH_TOKEN:
        print("ERROR: ANTHROPIC_AUTH_TOKEN not set")
        sys.exit(1)

    data = load_data()
    batches = build_batches(data)
    print(f"Total: {len(data)} diseases in {len(batches)} batches")

    # Load existing results
    all_results = {}
    for i in range(1, 100):
        path = f'{OUTPUT_DIR}/deepseek_v3_batch{i}.json'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for item in json.load(f):
                    all_results[item['disease']] = item['rating']
        except:
            break

    # Load reverify results
    for fname in ['deepseek_reverify_batch1.json', 'deepseek_reverify_batch2.json']:
        try:
            with open(f'{OUTPUT_DIR}/{fname}', 'r', encoding='utf-8') as f:
                for item in json.load(f):
                    all_results[item['disease']] = item['rating']
        except:
            pass

    print(f"Already verified: {len(all_results)} diseases")

    for batch_idx, batch in enumerate(batches):
        batch_diseases = [d[0] for d in batch]
        batch_num = batch_idx + 1

        # Skip if already done
        if batch_num == 1 or all(d in all_results for d in batch_diseases):
            continue

        print(f"\n[Batch {batch_num}/{len(batches)}] {len(batch)} diseases: {', '.join(batch_diseases[:3])}...")

        entries = [d[1] for d in batch]
        prompt = f"""请作为临床药学专家，快速评估以下每种疾病的推荐药物是否临床适当。对每种疾病，只给出评级（APPROPRIATE完全适当 / PARTIALLY部分适当 / INAPPROPRIATE不适当）。

格式: 疾病名: 评级

{chr(10).join(entries)}"""

        try:
            response_text = call_api(prompt)
            print(f"  Response: {response_text[:300]}...")

            batch_results = []
            for line in response_text.strip().split('\n'):
                line = line.strip()
                for rating in ['APPROPRIATE', 'PARTIALLY', 'INAPPROPRIATE']:
                    if rating in line:
                        disease = line.split(rating)[0].strip().rstrip('：:').strip()
                        disease = re.sub(r'^[\d\.\-\s]+', '', disease)
                        if disease and len(disease) < 15:
                            batch_results.append({'disease': disease, 'rating': rating})
                            all_results[disease] = rating
                            break

            # Fill in any missing diseases from the batch
            found = set(r['disease'] for r in batch_results)
            for d in batch_diseases:
                if d not in found:
                    print(f"  WARNING: {d} not found in response, trying heuristic...")
                    # Check if any line contains this disease
                    for line in response_text.split('\n'):
                        if d in line:
                            for rating in ['APPROPRIATE', 'PARTIALLY', 'INAPPROPRIATE']:
                                if rating in line:
                                    batch_results.append({'disease': d, 'rating': rating})
                                    all_results[d] = rating
                                    print(f"  Fixed: {d} -> {rating}")
                                    break
                            break

            # Save batch results
            out_path = f'{OUTPUT_DIR}/deepseek_v3_batch{batch_num}.json'
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(batch_results, f, ensure_ascii=False, indent=2)
            print(f"  Saved {len(batch_results)} ratings to batch{batch_num}.json")

        except Exception as e:
            print(f"  ERROR: {e}")
            time.sleep(5)
            continue

        time.sleep(1)  # Rate limiting

    # Final summary
    print(f"\n{'='*60}")
    print(f"VERIFICATION COMPLETE: {len(all_results)} diseases rated")
    from collections import Counter
    counts = Counter(all_results.values())
    print(f"  APPROPRIATE: {counts.get('APPROPRIATE', 0)}")
    print(f"  PARTIALLY: {counts.get('PARTIALLY', 0)}")
    print(f"  INAPPROPRIATE: {counts.get('INAPPROPRIATE', 0)}")

    # Save combined results
    combined = [{'disease': k, 'rating': v} for k, v in all_results.items()]
    with open(f'{OUTPUT_DIR}/deepseek_v3_all_204.json', 'w', encoding='utf-8') as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)
    print(f"\nCombined results saved to deepseek_v3_all_204.json")

if __name__ == "__main__":
    main()
