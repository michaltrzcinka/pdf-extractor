import pathlib

import pymupdf4llm

print("Hello World")
for pdf_file in pathlib.Path("data").iterdir():
    if pdf_file.is_file():
        md_text = pymupdf4llm.to_markdown(str(pdf_file))
        output_file = pathlib.Path("output_" + pdf_file.stem + ".md")
        output_file.write_bytes(md_text.encode())
