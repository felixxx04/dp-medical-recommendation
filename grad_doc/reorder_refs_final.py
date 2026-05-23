"""
Reorder references and renumber citations in the thesis document.
- Citations in body text are reordered to appear as [1], [2], [3]... sequentially
- Reference list is reordered to match
- Uncited references [11] and [12] are kept at the end
"""
import re
import copy

# --- Configuration ---
INPUT_XML = 'unpacked_cover_fixed/word/document.xml'
OUTPUT_XML = 'unpacked_cover_fixed/word/document.xml'

# Citation order of first appearance in body text
unique_citation_order = [2, 3, 4, 6, 7, 8, 5, 1, 9, 10, 15, 13, 14, 16, 18, 19, 20, 21, 22, 17, 23, 24, 25]
uncited_refs = [11, 12]

# Reference paragraph range (0-indexed in the paragraph list)
REF_PARA_START = 901
REF_PARA_END = 926  # exclusive

# --- Build mapping ---
old_to_new = {}
for new_num, old_num in enumerate(unique_citation_order, 1):
    old_to_new[old_num] = new_num
for i, old_num in enumerate(uncited_refs):
    old_to_new[old_num] = len(unique_citation_order) + i + 1

print("Mapping old -> new:")
for old in sorted(old_to_new.keys()):
    marker = " (uncited)" if old in uncited_refs else ""
    print(f"  [{old}] -> [{old_to_new[old]}]{marker}")

# --- Read XML ---
with open(INPUT_XML, 'r', encoding='utf-8') as f:
    content = f.read()

# --- Step 1: Replace citation numbers in body text ---
# All citations are in <w:t>[N]</w:t> format (verified earlier)
# Replace from highest to lowest to avoid double-replacement issues

# First, use temporary placeholders to avoid conflicts
# e.g., [5] -> [7] and [7] -> [5] would conflict if done sequentially
placeholder_map = {}
for old_num, new_num in old_to_new.items():
    placeholder_map[old_num] = f'__REF_{new_num}__'

# Replace [N] with placeholders
for old_num in sorted(old_to_new.keys(), reverse=True):
    old_pattern = f'[{old_num}]'
    new_placeholder = placeholder_map[old_num]
    content = content.replace(f'<w:t>[{old_num}]</w:t>', f'<w:t>{new_placeholder}</w:t>')

# Replace placeholders with final numbers
for old_num, new_num in old_to_new.items():
    placeholder = placeholder_map[old_num]
    content = content.replace(f'<w:t>{placeholder}</w:t>', f'<w:t>[{new_num}]</w:t>')

# Verify no placeholders remain
remaining = re.findall(r'__REF_\d+__', content)
if remaining:
    print(f"WARNING: {len(remaining)} placeholders remain!")
else:
    print("All citation placeholders replaced successfully")

# --- Step 2: Reorder reference paragraphs ---
paras = re.findall(r'<w:p\b[^>]*>.*?</w:p>', content, re.DOTALL)
print(f"Total paragraphs: {len(paras)}")

# Extract reference paragraphs
ref_paras = {}
for old_num in range(1, 26):
    para_idx = REF_PARA_START + old_num - 1
    ref_paras[old_num] = paras[para_idx]

# Build new order of reference paragraphs
new_ref_order = []
for new_num in range(1, 26):
    old_num = [k for k, v in old_to_new.items() if v == new_num][0]
    new_ref_order.append(ref_paras[old_num])

# Replace reference paragraphs in the XML
# We need to find the exact position of each reference paragraph and replace them in order
# The simplest approach: reconstruct the content by replacing the ref paragraph block

# Find the block of reference paragraphs in the original content
# Get the first and last ref paragraph strings to locate them
first_ref_para = paras[REF_PARA_START]
last_ref_para = paras[REF_PARA_END - 1]

# Find positions of all ref paragraphs
ref_block_start = None
ref_block_end = None

for i, para in enumerate(paras):
    if i == REF_PARA_START and para == ref_paras[1]:
        ref_block_start = content.find(para)
    if i == REF_PARA_END - 1 and para == ref_paras[25]:
        # Find the end of this paragraph
        pos = content.find(para)
        ref_block_end = pos + len(para)

if ref_block_start is None or ref_block_end is None:
    print("ERROR: Could not locate reference block!")
else:
    # Replace the entire reference block with reordered paragraphs
    new_ref_block = '\n'.join(new_ref_order)
    content = content[:ref_block_start] + new_ref_block + content[ref_block_end:]
    print("Reference paragraphs reordered successfully")

# --- Step 3: Verify ---
# Re-parse and check citation order
texts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', content)
full_text = ''.join(texts)
citations = re.findall(r'\[(\d+)\]', full_text)

# Check only body text citations (before the reference list)
# The reference list uses auto-numbering, so we only care about body text [N]
# Let's check if citations are now in sequential order of first appearance
seen = set()
unique_new = []
for c in citations:
    if c not in seen:
        seen.add(c)
        unique_new.append(c)

print(f"\nNew unique citation order: {unique_new}")

# Check if they're sequential (1, 2, 3, ...)
is_sequential = True
for i, c in enumerate(unique_new, 1):
    if int(c) != i:
        is_sequential = False
        print(f"  Out of order: expected [{i}], got [{c}]")

if is_sequential:
    print("All citations are now in sequential order!")

# --- Write output ---
with open(OUTPUT_XML, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nOutput written to {OUTPUT_XML}")
