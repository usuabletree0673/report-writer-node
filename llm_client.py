import os
import requests
from dotenv import load_dotenv
import openai

load_dotenv()

# ENV vars
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://localhost:8000/generate")

# Set up OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_text(prompt: str, backend="openai", max_tokens=800):
    if backend == "openai":
        return openai_generate(prompt, max_tokens)
    elif backend == "local":
        return local_generate(prompt, max_tokens)
    else:
        raise ValueError("Invalid backend")

def openai_generate(prompt, max_tokens):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a report-writing assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def local_generate(prompt, max_tokens):
    response = requests.post(LOCAL_LLM_URL, json={
        "prompt": prompt,
        "max_tokens": max_tokens
    })
    response.raise_for_status()
    return response.json().get("text", "").strip()
