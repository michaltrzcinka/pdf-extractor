import pathlib

import pymupdf4llm
from ai import extract_customer_name

for pdf_file in pathlib.Path("data").iterdir():
    if pdf_file.is_file():
        print("Processing file:", pdf_file)
        md_text = pymupdf4llm.to_markdown(str(pdf_file))
        customer_name = extract_customer_name(md_text)
        print("Customer name:", customer_name)
