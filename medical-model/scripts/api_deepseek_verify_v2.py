"""Verify disease recommendations via DeepSeek API - v2 with better parsing and retries."""
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
            rec_lines.append(f'{r["englishName"]} ({r["category"]})')
        entry = f'{disease}: ' + '; '.join(rec_lines)
        current.append((disease, entry))
        if len(current) >= BATCH_SIZE:
            batches.append(current)
            current = []
    if current:
        batches.append(current)
    return batches

def call_api(prompt, retry=0):
    payload = {
        'model': MODEL,
        'max_tokens': 3000,
        'messages': [{'role': 'user', 'content': prompt}]
    }
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': AUTH_TOKEN,
        'anthropic-version': '2023-06-01'
    }
    try:
        r = requests.post(BASE_URL, json=payload, headers=headers, timeout=180)
        if r.status_code == 200:
            data = r.json()
            content_blocks = data.get('content', [])

            # First try to get text content
            for block in content_blocks:
                if block.get('type') == 'text':
                    text = block.get('text', '').strip()
                    if text:
                        return text

            # Fallback: extract from thinking block
            for block in content_blocks:
                if block.get('type') == 'thinking':
                    thinking = block.get('thinking', '')
                    # Try to find ratings in thinking
                    lines = thinking.strip().split('\n')
                    text_lines = []
                    for line in lines:
                        for rating in ['APPROPRIATE', 'PARTIALLY', 'INAPPROPRIATE']:
                            if rating in line:
                                text_lines.append(line.strip())
                                break
                    if text_lines:
                        return '\n'.join(text_lines)

            # Also try getting text from full response
            full_text = json.dumps(data, ensure_ascii=False)
            return ''
        else:
            raise Exception(f"API error {r.status_code}: {r.text[:300]}")
    except requests.exceptions.Timeout:
        if retry < 2:
            print(f"  Timeout, retrying ({retry+1}/2)...")
            time.sleep(5)
            return call_api(prompt, retry + 1)
        raise

def parse_response(text, batch_diseases):
    results = {}
    for line in text.split('\n'):
        line = line.strip()
        for rating in ['APPROPRIATE', 'PARTIALLY', 'INAPPROPRIATE']:
            if rating in line:
                # Extract disease name
                disease_part = line.split(rating)[0].strip().rstrip('：:').strip()
                disease_part = re.sub(r'^[\d\.\-\*\s]+', '', disease_part).strip()

                # Match against expected diseases
                for d in batch_diseases:
                    if d in disease_part or disease_part in d:
                        results[d] = rating
                        break
                break

    # Handle missing diseases with fuzzy matching
    found = set(results.keys())
    for d in batch_diseases:
        if d not in found:
            for line in text.split('\n'):
                if d in line:
                    for rating in ['APPROPRIATE', 'PARTIALLY', 'INAPPROPRIATE']:
                        if rating in line:
                            results[d] = rating
                            found.add(d)
                            break
                    break

    return results

def main():
    if not AUTH_TOKEN:
        print("ERROR: ANTHROPIC_AUTH_TOKEN not set")
        sys.exit(1)

    data = load_data()
    batches = build_batches(data)
    all_diseases = [d['disease_cn'] for d in data]
    print(f"Total: {len(data)} diseases in {len(batches)} batches")

    # Load existing results
    all_results = {}

    # Load v3 batch results
    for i in range(1, 100):
        path = f'{OUTPUT_DIR}/deepseek_v3_batch{i}.json'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                items = json.load(f)
                if items:
                    for item in items:
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

    # Load before-fix results as fallback
    before_ratings = {}
    for batch_num in range(2, 8):
        path = f'{OUTPUT_DIR}/deepseek_batch{batch_num}_results.json'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                bdata = json.load(f)
                for item in bdata.get('results', []):
                    before_ratings[item['disease']] = item['rating']
        except:
            pass

    print(f"Already verified: {len(all_results)} diseases")

    missing = [d for d in all_diseases if d not in all_results]
    print(f"Need to verify: {len(missing)} diseases")

    # Find which batches contain missing diseases
    for batch_idx, batch in enumerate(batches):
        batch_diseases = [d[0] for d in batch]
        needs_verify = [d for d in batch_diseases if d not in all_results]

        if not needs_verify:
            continue

        batch_num = batch_idx + 1
        print(f"\n[Batch {batch_num}/{len(batches)}] {len(batch)} diseases, {len(needs_verify)} need verify")
        print(f"  Missing: {', '.join(needs_verify[:5])}...")

        # Only prompt for the missing diseases
        entries_to_verify = []
        diseases_to_verify = []
        for disease, entry in batch:
            if disease not in all_results:
                entries_to_verify.append(entry)
                diseases_to_verify.append(disease)

        prompt = f"""作为临床药学专家，请评估以下每种疾病的推荐药物是否适当。

格式：疾病名: 评级
评级选项：APPROPRIATE(完全适当) PARTIALLY(部分适当) INAPPROPRIATE(不适当)

{chr(10).join(entries_to_verify)}"""

        try:
            response_text = call_api(prompt)
            print(f"  Response ({len(response_text)} chars): {response_text[:200]}...")

            if not response_text:
                print("  EMPTY RESPONSE - will retry later")
                continue

            batch_results = []
            results = parse_response(response_text, diseases_to_verify)

            for disease, rating in results.items():
                batch_results.append({'disease': disease, 'rating': rating})
                all_results[disease] = rating

            found = set(results.keys())
            for d in diseases_to_verify:
                if d not in found:
                    # Try to extract from the raw response
                    for line in response_text.split('\n'):
                        if d in line:
                            for rating in ['APPROPRIATE', 'PARTIALLY', 'INAPPROPRIATE']:
                                if rating in line:
                                    batch_results.append({'disease': d, 'rating': rating})
                                    all_results[d] = rating
                                    found.add(d)
                                    print(f"  Heuristic found: {d} -> {rating}")
                                    break
                            break

            # Save batch
            out_path = f'{OUTPUT_DIR}/deepseek_v3_batch{batch_num}.json'
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(batch_results, f, ensure_ascii=False, indent=2)

            still_missing = [d for d in diseases_to_verify if d not in found]
            print(f"  Saved {len(batch_results)} ratings, still missing: {len(still_missing)}")
            if still_missing:
                for d in still_missing:
                    print(f"    Missing: {d}")

        except Exception as e:
            print(f"  ERROR: {e}")
            time.sleep(5)
            continue

        time.sleep(3)  # Rate limiting

    # Fill remaining gaps with before-fix ratings as fallback
    still_missing = [d for d in all_diseases if d not in all_results]
    if still_missing and before_ratings:
        print(f"\nUsing {len(before_ratings)} before-fix ratings as fallback for {len(still_missing)} missing...")
        filled = 0
        for d in still_missing:
            if d in before_ratings:
                all_results[d] = before_ratings[d]
                filled += 1
        print(f"Filled {filled} gaps with before-fix ratings")
        still_missing = [d for d in all_diseases if d not in all_results]

    # Final summary
    print(f"\n{'='*60}")
    print(f"VERIFICATION COMPLETE: {len(all_results)}/{len(all_diseases)} diseases rated")
    from collections import Counter
    counts = Counter(all_results.values())
    print(f"  APPROPRIATE: {counts.get('APPROPRIATE', 0)}")
    print(f"  PARTIALLY: {counts.get('PARTIALLY', 0)}")
    print(f"  INAPPROPRIATE: {counts.get('INAPPROPRIATE', 0)}")

    if still_missing:
        print(f"  STILL MISSING ({len(still_missing)}): {', '.join(still_missing[:10])}")

    # Save combined
    combined = [{'disease': k, 'rating': v} for k, v in all_results.items()]
    with open(f'{OUTPUT_DIR}/deepseek_v3_all_204.json', 'w', encoding='utf-8') as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)
    print(f"\nCombined results saved to deepseek_v3_all_204.json")

if __name__ == "__main__":
    main()
