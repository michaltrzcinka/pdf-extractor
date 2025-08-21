import io

import pymupdf
import pytest


@pytest.fixture
def pdf_bytes():
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Invoice: 123\nCustomer: Alice")
    buf = io.BytesIO()
    doc.save(buf)
    doc.close()
    buf.seek(0)
    return buf


class _FakeMessage:
    def __init__(self, content):
        self.content = content


class _FakeChoice:
    def __init__(self, message):
        self.message = message


class _FakeResponse:
    def __init__(self, content):
        self.choices = [_FakeChoice(_FakeMessage(content))]


class _Recorder:
    def __init__(self, content):
        self._content = content
        self.messages = None


class _FakeCompletions:
    def __init__(self, recorder):
        self._recorder = recorder

    def create(self, model, messages):
        self._recorder.messages = messages
        return _FakeResponse(self._recorder._content)


class _FakeChat:
    def __init__(self, recorder):
        self.completions = _FakeCompletions(recorder)


class FakeOpenAIClient:
    def __init__(self, content):
        self._recorder = _Recorder(content)
        self.chat = _FakeChat(self._recorder)

    @property
    def recorded_messages(self):
        return self._recorder.messages


@pytest.fixture
def fake_openai_client_factory():
    def _factory(content):
        return FakeOpenAIClient(content)

    return _factory
