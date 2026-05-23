"""Center all formulas in the thesis document.

Handles two cases:
1. Standalone formula paragraphs: center alignment + right tab stop for equation number
2. Mixed text+formula paragraphs: split into text (JUSTIFY) + formula (CENTER) paragraphs
"""
import sys
import copy
from lxml import etree
from docx import Document
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
nsmap = {'w': W, 'm': M}

INPUT = '晋修慧初稿_审阅修改版.docx'
OUTPUT = '晋修慧初稿_审阅修改版_centered.docx'


def find_omath_position(children):
    """Find the index of the first m:oMath element."""
    for ci, child in enumerate(children):
        tag = etree.QName(child.tag).localname
        if tag == 'oMath':
            return ci
    return None


def has_text_content(elem):
    """Check if a w:r element has non-empty text content."""
    t = elem.find(f'{{{W}}}t')
    return t is not None and t.text and t.text.strip()


def get_run_text(elem):
    """Get text from a w:r element."""
    t = elem.find(f'{{{W}}}t')
    return t.text if t is not None and t.text else ''


def has_br(elem):
    """Check if a w:r element contains a line break."""
    return elem.find(f'{{{W}}}br') is not None


def create_paragraph_element(alignment=None):
    """Create a new w:p element with optional alignment."""
    p = etree.SubElement(etree.Element('dummy'), f'{{{W}}}p')
    pPr = etree.SubElement(p, f'{{{W}}}pPr')

    if alignment is not None:
        jc = etree.SubElement(pPr, f'{{{W}}}jc')
        jc.set(f'{{{W}}}val', alignment)

    return p


def set_paragraph_alignment(p_elem, alignment):
    """Set paragraph alignment (center, left, justify, etc.)."""
    pPr = p_elem.find(f'{{{W}}}pPr')
    if pPr is None:
        pPr = etree.SubElement(p_elem, f'{{{W}}}pPr')
        p_elem.insert(0, pPr)

    jc = pPr.find(f'{{{W}}}jc')
    if jc is None:
        jc = etree.SubElement(pPr, f'{{{W}}}jc')
    jc.set(f'{{{W}}}val', alignment)


def add_right_tab_stop(p_elem, position_twips=8300):
    """Add a right-aligned tab stop at the given position (in twips)."""
    pPr = p_elem.find(f'{{{W}}}pPr')
    if pPr is None:
        pPr = etree.SubElement(p_elem, f'{{{W}}}pPr')
        p_elem.insert(0, pPr)

    tabs = pPr.find(f'{{{W}}}tabs')
    if tabs is None:
        tabs = etree.SubElement(pPr, f'{{{W}}}tabs')

    # Remove existing right tab stops
    for tab in tabs.findall(f'{{{W}}}tab'):
        if tab.get(f'{{{W}}}val') == 'right':
            tabs.remove(tab)

    tab = etree.SubElement(tabs, f'{{{W}}}tab')
    tab.set(f'{{{W}}}val', 'right')
    tab.set(f'{{{W}}}pos', str(position_twips))


def clean_tabs_in_formula(p_elem, omath_idx):
    """Remove excessive tabs between formula and equation number, keep only one."""
    children = list(p_elem)
    # Find runs after oMath that only contain tabs or whitespace
    # Keep one tab run for the right tab stop, remove the rest
    runs_to_remove = []
    found_eq_num = False
    tab_count = 0

    for ci in range(omath_idx + 1, len(children)):
        child = children[ci]
        tag = etree.QName(child.tag).localname
        if tag != 'r':
            continue

        text = get_run_text(child)
        has_tab = child.find(f'{{{W}}}tab') is not None

        if has_tab and not text.strip():
            tab_count += 1
            if tab_count > 1:
                runs_to_remove.append(child)
        elif text.strip() and '(' in text:
            # This is the equation number
            found_eq_num = True
            break
        elif text.strip() and not has_tab:
            # Non-tab text after formula (like a space)
            if not text.strip() or text.strip() == ' ':
                # Just whitespace, can remove
                if not found_eq_num:
                    runs_to_remove.append(child)

    for run in runs_to_remove:
        p_elem.remove(run)


def copy_paragraph_properties(src_pPr, dst_pPr):
    """Copy paragraph properties from src to dst, excluding alignment and tabs."""
    if src_pPr is None:
        return
    for child in src_pPr:
        tag = etree.QName(child.tag).localname
        # Skip jc (alignment) and tabs - we'll set our own
        if tag in ('jc', 'tabs'):
            continue
        child_copy = copy.deepcopy(child)
        # Insert before jc if it exists
        jc = dst_pPr.find(f'{{{W}}}jc')
        if jc is not None:
            jc.addprevious(child_copy)
        else:
            dst_pPr.append(child_copy)


def main():
    doc = Document(INPUT)
    body = doc.element.body

    # Collect all paragraph elements
    all_paras = list(doc.paragraphs)

    # Process in reverse order so insertions don't affect indices
    for i in range(len(all_paras) - 1, -1, -1):
        para = all_paras[i]
        xml_str = para._element.xml
        if 'oMath' not in xml_str:
            continue

        p_elem = para._element
        children = list(p_elem)
        omath_idx = find_omath_position(children)

        if omath_idx is None:
            continue

        # Classify: standalone or mixed
        has_text_before = False
        text_before_elements = []  # Elements before oMath (excluding pPr)
        for ci in range(1, omath_idx):
            child = children[ci]
            tag = etree.QName(child.tag).localname
            text_before_elements.append(child)
            if tag == 'r' and has_text_content(child):
                has_text_before = True

        # Find equation number run index
        eq_num_idx = None
        for ci in range(omath_idx + 1, len(children)):
            child = children[ci]
            tag = etree.QName(child.tag).localname
            if tag == 'r':
                text = get_run_text(child)
                if '(' in text and any(c.isdigit() for c in text):
                    eq_num_idx = ci
                    break

        # Check for text after equation number
        has_text_after = False
        text_after_elements = []
        if eq_num_idx is not None:
            # Look for BR after eq number, then text
            found_br_after = False
            for ci in range(eq_num_idx + 1, len(children)):
                child = children[ci]
                tag = etree.QName(child.tag).localname
                if tag == 'r':
                    if has_br(child):
                        found_br_after = True
                        text_after_elements.append(child)
                    elif found_br_after and has_text_content(child):
                        has_text_after = True
                        text_after_elements.append(child)
                    elif found_br_after:
                        text_after_elements.append(child)

        # Formula group: oMath + tabs + eq number (+ any runs between)
        formula_elements = []
        start = omath_idx
        end = (eq_num_idx + 1) if eq_num_idx is not None else omath_idx + 1
        for ci in range(start, end):
            formula_elements.append(children[ci])

        print(f"Para #{i}: before={has_text_before}, after={has_text_after}, "
              f"omath_idx={omath_idx}, eq_idx={eq_num_idx}")

        if has_text_before or has_text_after:
            # === SPLIT THE PARAGRAPH ===
            parent = p_elem.getparent()
            p_idx = list(parent).index(p_elem)

            # Get original paragraph properties
            orig_pPr = p_elem.find(f'{{{W}}}pPr')

            # 1. Create "text before" paragraph
            if has_text_before:
                p_before = etree.Element(f'{{{W}}}p')
                pPr_before = etree.SubElement(p_before, f'{{{W}}}pPr')
                if orig_pPr is not None:
                    copy_paragraph_properties(orig_pPr, pPr_before)
                set_paragraph_alignment(p_before, 'both')  # JUSTIFY

                # Move text-before elements (runs + BR run before oMath)
                for elem in text_before_elements:
                    # Don't include the BR that precedes the formula
                    if etree.QName(elem.tag).localname == 'r' and has_br(elem):
                        # This BR separates text from formula, skip it
                        continue
                    p_before.append(copy.deepcopy(elem))

                parent.insert(p_idx, p_before)
                p_idx += 1
                print(f"  Created 'before' paragraph")

            # 2. Create formula paragraph (centered)
            p_formula = etree.Element(f'{{{W}}}p')
            pPr_formula = etree.SubElement(p_formula, f'{{{W}}}pPr')
            if orig_pPr is not None:
                copy_paragraph_properties(orig_pPr, pPr_formula)
            set_paragraph_alignment(p_formula, 'center')
            add_right_tab_stop(p_formula, 8300)

            # Add oMath
            for elem in formula_elements:
                tag = etree.QName(elem.tag).localname
                if tag == 'oMath':
                    p_formula.append(copy.deepcopy(elem))
                    break  # Only add the first oMath

            # Add single tab
            tab_run = etree.SubElement(p_formula, f'{{{W}}}r')
            etree.SubElement(tab_run, f'{{{W}}}tab')

            # Add equation number
            if eq_num_idx is not None:
                eq_run = copy.deepcopy(children[eq_num_idx])
                # Clean the run - remove any tabs inside
                for tab in eq_run.findall(f'{{{W}}}tab'):
                    eq_run.remove(tab)
                p_formula.append(eq_run)

            parent.insert(p_idx, p_formula)
            p_idx += 1
            print(f"  Created centered formula paragraph")

            # 3. Create "text after" paragraph (if needed)
            if has_text_after:
                p_after = etree.Element(f'{{{W}}}p')
                pPr_after = etree.SubElement(p_after, f'{{{W}}}pPr')
                if orig_pPr is not None:
                    copy_paragraph_properties(orig_pPr, pPr_after)
                set_paragraph_alignment(p_after, 'both')  # JUSTIFY

                for elem in text_after_elements:
                    tag = etree.QName(elem.tag).localname
                    if tag == 'r':
                        if has_br(elem):
                            continue  # Skip the BR separator
                        if has_text_content(elem):
                            p_after.append(copy.deepcopy(elem))
                        # Skip empty runs with just tabs

                if len(list(p_after)) > 1:  # More than just pPr
                    parent.insert(p_idx, p_after)
                    print(f"  Created 'after' paragraph")
                else:
                    print(f"  Skipped empty 'after' paragraph")

            # Remove original paragraph
            parent.remove(p_elem)
            print(f"  Removed original paragraph")

        else:
            # === STANDALONE FORMULA - JUST CENTER IT ===
            set_paragraph_alignment(p_elem, 'center')
            add_right_tab_stop(p_elem, 8300)
            clean_tabs_in_formula(p_elem, omath_idx)
            print(f"  Centered standalone formula")

    doc.save(OUTPUT)
    print(f"\nSaved to {OUTPUT}")


if __name__ == '__main__':
    main()
