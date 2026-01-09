import os
from dotenv import load_dotenv
import requests

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_llm(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 200,
        "stop": ["[/s]", "[s]", "###"]
    }

    r = requests.post(url, headers=headers, json=payload, timeout=30)

    if r.status_code != 200:
        return "LLM_ERROR"

    content = r.json()["choices"][0]["message"]["content"]
    
    # Clean up any remaining special tokens
    content = content.replace("[/s]", "").replace("[s]", "").strip()
    
    return content
