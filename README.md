# PDF Extractor

Small Streamlit app that extracts specific fields from PDFs. It converts a PDF to Markdown using MuPDF, 
asks a local LLM via Ollama (through the OpenAI SDK) to fill requested fields, and renders the result as 
a clean HTML table.

Initially, I tried implementing the extraction using regular MyPDF code, but it was very tedious, complex and brittle.
After switching to a fairly small, locally hosted LLM and using a simple prompt, I got much better results.

This is obviously not production-ready code, but an early prototype. If we want to grow it into something serious,
the next steps would be:

1. Split this app into backend (with an API and a message queue) and frontend.
1. Add a database and an ORM library like SQLAlchemy to store the extraction requests, progress and responses.
1. Consider replacing OpenAI library with LangChain.
1. Deploy the LLM to a separate server or consider using LLM APIs if feasible.
1. Prepare an evaluation script that tests the extraction performance. Hook that script to CI/CD.
1. Report errors to an error monitoring solution like Sentry.
1. Report key metrics to an observability platform like Datadog or ELK.

## Quick start

- **Requirements**
  - Python 3.11+
  - macOS/Linux
  - Ollama running locally on port 11434

### 1) Create venv and install deps

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

For development and tests:

```bash
pip install -r requirements-dev.txt
```

### 2) Install and start Ollama

Install Ollama and pull the model used by the app.

```bash
brew install ollama
ollama serve
ollama pull gpt-oss:20b
```

If you already have Ollama, just ensure it’s running and the model is pulled. The app expects Ollama at `http://localhost:11434` and uses model `gpt-oss:20b`. No API keys are needed.

### 3) Run the app (Streamlit)

```bash
streamlit run pdfextractor/main.py
```

In the UI:
- Select fields you want to extract
- Upload a PDF
- Click Extract

## Run tests

```bash
pytest -q
```

With coverage:

```bash
pytest --cov=pdfextractor -q
```

## Notes

- The LLM call is made via the OpenAI SDK pointed at the local Ollama endpoint.
- If extraction fails to connect, verify `ollama serve` is running and the model is available.
