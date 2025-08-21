import json
from io import BytesIO

import pymupdf
import pymupdf4llm
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",  # Local Ollama API
    api_key="ollama",  # Dummy key
)


def extract(file: BytesIO, fields: list[str]) -> dict[str, str]:
    doc = pymupdf.open(stream=file.getvalue(), filetype="pdf")
    md_text = pymupdf4llm.to_markdown(doc)
    extracted_fields_str = call_llm(md_text, fields)
    print("extracted_fields_str", extracted_fields_str)
    extracted_fields = json.loads(extracted_fields_str)
    return extracted_fields


def call_llm(document: str, fields: list[str]) -> str:
    field_names = ", ".join(fields)
    output_example = json.dumps({field: "Value" for field in fields})

    prompt = f"""
    You are a helpful assistant that extracts fields from a markdown document.
    Here is the markdown document:

    ```markdown
    {document}
    ```

    The fields to extract are: {field_names}
    If you can't find a value for a field, return "" for that key.

    Return a JSON object with the following keys:
    {output_example}

    Make sure to return just the JSON, nothing else (no "```json" or "```").
    """

    print("prompt", prompt)

    response = client.chat.completions.create(
        model="gpt-oss:20b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
