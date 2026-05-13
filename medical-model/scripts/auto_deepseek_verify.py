"""Automate DeepSeek verification of disease recommendations using Playwright.
Submits batches to chat.deepseek.com and extracts the ratings."""
import json
import time
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RETEST_DATA = "verification_results_v2/retest_204_after_fix_v3.json"
OUTPUT_DIR = "verification_results_v2"
BATCH_SIZE = 15

def create_batches():
    with open(RETEST_DATA, 'r', encoding='utf-8') as f:
        data = json.load(f)

    batches = []
    current_batch = []

    for d in data:
        disease = d['disease_cn']
        recs = d['recommendations'][:4]
        rec_lines = []
        for j, r in enumerate(recs):
            rec_lines.append(f'{j+1}. {r["englishName"]} ({r["category"]}) - matched: {r["matchedDisease"]}')
        entry = f'疾病: {disease}\n推荐药物:\n' + '\n'.join(rec_lines)
        current_batch.append((disease, entry))

        if len(current_batch) >= BATCH_SIZE:
            batches.append(current_batch)
            current_batch = []

    if current_batch:
        batches.append(current_batch)

    return batches

def build_prompt(batch):
    entries = [e[1] for e in batch]
    prompt = '请作为临床药学专家，评估以下每种疾病的推荐药物是否临床适当。对每种疾病，给出评级：APPROPRIATE(完全适当)、PARTIALLY(部分适当/有更好选择)、INAPPROPRIATE(不适当)。只需给出疾病名和评级。\n\n'
    prompt += '\n---\n'.join(entries)
    return prompt

def parse_response(text):
    """Extract disease: rating pairs from DeepSeek response."""
    results = {}
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        for rating in ['APPROPRIATE', 'PARTIALLY', 'INAPPROPRIATE']:
            if rating in line:
                # Extract disease name (everything before the rating)
                disease = line.replace(rating, '').strip().rstrip('：:').strip()
                # Remove leading markers like "1.", "-", etc.
                disease = re.sub(r'^[\d\.\-\s]+', '', disease).strip()
                if disease and len(disease) < 20:
                    results[disease] = rating
                break
    return results

def main():
    batches = create_batches()
    print(f"Total batches: {len(batches)}")

    # Show what's already done
    all_results = {}

    # Load existing results
    for i in range(1, 22):  # up to 21 batches
        path = f'{OUTPUT_DIR}/deepseek_v3_batch{i}.json'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                existing = json.load(f)
                for item in existing:
                    all_results[item['disease']] = item['rating']
        except:
            pass

    done_count = len(all_results)
    print(f"Already verified: {done_count} diseases")

    # Find which batches remain
    remaining_batches = []
    for i, batch in enumerate(batches):
        batch_diseases = set(d[0] for d in batch)
        if not batch_diseases.issubset(all_results.keys()):
            remaining_batches.append((i, batch))

    print(f"Remaining batches: {len(remaining_batches)}")

    if not remaining_batches:
        print("All batches complete!")
        return

    # Print the prompt for the next batch so it can be copied
    batch_idx, batch = remaining_batches[0]
    prompt = build_prompt(batch)
    diseases_in_batch = [d[0] for d in batch]
    batch_num = batch_idx + 1

    print(f"\n{'='*60}")
    print(f"Next: Batch {batch_num}/{len(batches)} ({len(batch)} diseases)")
    print(f"Diseases: {', '.join(diseases_in_batch[:5])}...")
    print(f"{'='*60}")
    print(f"\nPrompt for batch {batch_num} ({len(prompt)} chars):")
    print(prompt[:200] + "...")

    # Save prompt to file
    prompt_path = f'{OUTPUT_DIR}/deepseek_v3_batch{batch_num}_prompt.txt'
    with open(prompt_path, 'w', encoding='utf-8') as f:
        f.write(prompt)
    print(f"\nFull prompt saved to: {prompt_path}")


if __name__ == "__main__":
    main()
