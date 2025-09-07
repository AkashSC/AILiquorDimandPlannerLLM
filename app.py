import os
import requests
import streamlit as st

# -----------------------------
# LLM Response Function (Groq)
# -----------------------------
def get_llm_response(prompt: str) -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "❌ GROQ_API_KEY environment variable not set in Render."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",   # other options: llama3-70b-8192, mixtral-8x7b-32768
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant for liquor demand planning."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.HTTPError as http_err:
