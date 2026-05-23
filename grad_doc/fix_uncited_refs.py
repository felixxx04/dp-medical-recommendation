"""
Fix citations: add [24] and [25] references in body text,
and remove the stale [11] cross-ref from P109.
"""
import re

with open('unpacked_cover_fixed/word/document.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# === Fix 1: Remove the stale [11] cross-ref from P109 ===
# After our earlier modification, P109 has:
# ... [24] ... text ... [25] ... [11] ... text
# The [11] (REF _Ref10511) is stale and needs to be removed

# Find the REF _Ref10511 block in P109 and remove it
# Pattern: <w:r>...<w:vertAlign w:val="superscript"/>...</w:rPr>
#   <w:fldChar w:fldCharType="begin"/>
#   <w:instrText> REF _Ref10511 \r \h </w:instrText>
#   <w:fldChar w:fldCharType="separate"/>
#   <w:t>[11]</w:t>
#   <w:fldChar w:fldCharType="end"/>
# </w:r>

# Find the specific _Ref10511 block
ref10511_pattern = r'<w:r>\s*<w:rPr>\s*<w:rFonts[^/]*/>\s*<w:sz w:val="24"/>\s*<w:vertAlign w:val="superscript"/>\s*</w:rPr>\s*<w:fldChar w:fldCharType="begin"/>\s*<w:instrText xml:space="preserve"> REF _Ref10511 \\r \\h </w:instrText><w:fldChar w:fldCharType="separate"/><w:t>\[11\]</w:t><w:fldChar w:fldCharType="end"/></w:r>'

match = re.search(ref10511_pattern, content, re.DOTALL)
if match:
    content = content[:match.start()] + content[match.end():]
    print(f"Removed stale [11] cross-ref (REF _Ref10511) from P109 at pos {match.start()}")
else:
    print("WARNING: Could not find stale [11] cross-ref pattern")
    # Try simpler approach - find by unique text
    simple_pattern = '> REF _Ref10511 '
    pos = content.find(simple_pattern)
    if pos >= 0:
        # Find the containing <w:r>...</w:r>
        run_start = content.rfind('<w:r>', 0, pos)
        run_end = content.find('</w:r>', pos) + 5
        removed = content[run_start:run_end]
        content = content[:run_start] + content[run_end:]
        print(f"Removed stale [11] cross-ref using simple search at pos {run_start}")
    else:
        print("ERROR: _Ref10511 not found at all!")

# === Fix 2: Add [24] cross-ref in P121 ===
# P121 has: "提出了适用于实时场景的隐私保护方案" followed by superscript "。"
# We need to change the superscript "。" to regular "。" and add [24] cross-ref

# Find the specific run in P121
# Current: <w:t>提出了适用于实时场景的隐私保护方案</w:t>
# followed by: <w:r>...superscript...<w:t>。</w:t></w:r>
# followed by: <w:r>...<w:t>这些研究为医疗数据隐私保护提供了技术支撑</w:t></w:r>

# Strategy: Find the text "提出了适用于实时场景的隐私保护方案" in P121 context
# (not in P109 which already has [24])

p121_key = '提出了适用于实时场景的隐私保护方案</w:t>\n      </w:r>\n      <w:r>\n        <w:rPr>\n          <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="宋体" w:cs="Times New Roman"/>\n          <w:b w:val="0"/>\n          <w:sz w:val="24"/>\n          <w:vertAlign w:val="superscript"/>\n        </w:rPr>\n        <w:t>。</w:t>'

p121_replacement = '提出了适用于实时场景的隐私保护方案</w:t>\n      </w:r>\n      <w:r>\n        <w:rPr>\n          <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="宋体" w:cs="Times New Roman"/>\n          <w:b w:val="0"/>\n          <w:sz w:val="24"/>\n          <w:vertAlign w:val="superscript"/>\n        </w:rPr>\n        <w:fldChar w:fldCharType="begin"/>\n      <w:instrText xml:space="preserve"> REF _Ref10051 \\r \\h </w:instrText><w:fldChar w:fldCharType="separate"/><w:t>[24]</w:t><w:fldChar w:fldCharType="end"/></w:r>\n      <w:r>\n        <w:rPr>\n          <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="宋体" w:cs="Times New Roman"/>\n          <w:b w:val="0"/>\n          <w:sz w:val="24"/>\n          <w:vertAlign w:val="baseline"/>\n        </w:rPr>\n        <w:t>。</w:t>'

if p121_key in content:
    content = content.replace(p121_key, p121_replacement)
    print("Added [24] cross-ref in P121")
else:
    print("WARNING: P121 pattern not found exactly")
    # Try a simpler approach - just find the superscript period after 隐私保护方案
    # in the P121 context (after [10])
    pass

# === Write output ===
with open('unpacked_cover_fixed/word/document.xml', 'w', encoding='utf-8') as f:
    f.write(content)

print("XML updated successfully")
