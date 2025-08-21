import json

import pytest

from pdfextractor import extractor


def test_extract_happy_path_returns_parsed_dict(
    monkeypatch, pdf_bytes, fake_openai_client_factory
):
    fields = ["invoice_number", "customer_name"]
    client = fake_openai_client_factory(
        json.dumps({"invoice_number": "123", "customer_name": "Alice"})
    )
    monkeypatch.setattr(extractor, "client", client)
    result = extractor.extract(pdf_bytes, fields)
    assert result == {"invoice_number": "123", "customer_name": "Alice"}


def test_extract_passes_pdf_markdown_and_fields_to_openai(
    monkeypatch, pdf_bytes, fake_openai_client_factory
):
    fields = ["invoice_number", "customer_name"]
    client = fake_openai_client_factory(
        json.dumps({"invoice_number": "123", "customer_name": "Alice"})
    )
    monkeypatch.setattr(extractor, "client", client)
    extractor.extract(pdf_bytes, fields)
    messages = client.recorded_messages
    assert messages is not None and len(messages) >= 2
    user_msg = messages[-1]["content"]
    assert "Invoice: 123" in user_msg
    assert "invoice_number, customer_name" in user_msg


def test_extract_handles_invalid_json_from_llm(
    monkeypatch, pdf_bytes, fake_openai_client_factory
):
    fields = ["invoice_number", "customer_name"]
    client = fake_openai_client_factory("not-a-json")
    monkeypatch.setattr(extractor, "client", client)
    with pytest.raises(json.JSONDecodeError):
        extractor.extract(pdf_bytes, fields)


def test_extract_allows_partial_fields_from_llm(
    monkeypatch, pdf_bytes, fake_openai_client_factory
):
    fields = ["invoice_number", "customer_name"]
    client = fake_openai_client_factory(json.dumps({"invoice_number": "123"}))
    monkeypatch.setattr(extractor, "client", client)
    result = extractor.extract(pdf_bytes, fields)
    assert result == {"invoice_number": "123"}
