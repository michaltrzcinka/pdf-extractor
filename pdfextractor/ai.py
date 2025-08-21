from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",  # Local Ollama API
    api_key="ollama",  # Dummy key
)


def extract_customer_name(markdown):
    prompt = f"""
    You are a helpful assistant that extracts the customer name from a markdown document.
    Here is the markdown document:
    {markdown}
    Return the customer name in the following format:
    {{
        "customer_name": "Customer Name",
        "confidence": 0.95
    }}
    """
    response = client.chat.completions.create(
        model="gpt-oss:20b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
