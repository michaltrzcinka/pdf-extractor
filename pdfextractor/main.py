import pathlib

import pymupdf


def find_block_to_right(page, label, min_overlap_ratio=0.3, epsilon=1.0):
    blocks = page.get_text("blocks")
    label_blocks = []
    for b in blocks:
        x0, y0, x1, y1, text = b[:5]
        if text and label.lower() in text.lower():
            label_blocks.append((x0, y0, x1, y1, text))
    print("label_blocks", label_blocks)
    if not label_blocks:
        return None
    tx0, ty0, tx1, ty1, ttext = sorted(label_blocks, key=lambda t: (t[1], t[0]))[0]
    print(f"tx0: {tx0}, tx1: {tx1}, ty0: {ty0}, ty1: {ty1}")
    candidates = []
    for b in blocks:
        x0, y0, x1, y1, text = b[:5]
        print(f"text: {text}")
        print(f"x0: {x0}, x1: {x1}, y0: {y0}, y1: {y1}")
        if x0 > tx0 and x1 < tx1 and y0 >= ty0 and y1 <= ty1:
            candidates.append((x0, y0, x1, y1, text))
    print("candidates", candidates)
    if not candidates:
        return None
    cx0, cy0, cx1, cy1, ctext = sorted(candidates, key=lambda c: (c[0] - tx1, c[1]))[0]
    return (cx0, cy0, cx1, cy1, ctext)


for pdf_file in pathlib.Path("data").iterdir():
    if (
        pdf_file.is_file()
        and pdf_file.stem == "CBZ TOUCH MANUAL REGISTRATION FORM filled"
    ):
        doc = pymupdf.open(str(pdf_file))
        page = doc[0]
        result = find_block_to_right(page, "Customer Name")
        if result:
            print(result[4].strip())
        else:
            print("No right-adjacent block found")
