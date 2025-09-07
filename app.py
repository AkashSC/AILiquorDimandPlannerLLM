import os
import json
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

    clean_prompt = prompt.strip()
    if not clean_prompt:
        return "⚠️ Please enter a valid question."

    payload = {
        "model": "llama-3.1-8b-instant",  # ✅ supported Groq model
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant for liquor demand planning."},
            {"role": "user", "content": clean_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            # Show full Groq error JSON for debugging
            try:
                err_data = response.json()
                return f"⚠️ API Error:\n```json\n{json.dumps(err_data, indent=2)}\n```"
            except Exception:
                return f"⚠️ HTTP {response.status_code}: {response.text}"

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ Unexpected Error: {e}"

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Liquor Demand Planner", layout="wide")
st.title("🍷 Liquor Demand Planner with AI Assistant")

# Sidebar - AI Q&A
st.sidebar.header("🔍 Ask the AI")
user_query = st.sidebar.text_area(
    "Type your question (e.g., demand trends, inventory tips, seasonal forecasts):",
    placeholder="Example: What will be the demand for whiskey during Diwali season?"
)

if st.sidebar.button("Get AI Advice"):
    if user_query.strip():
        with st.spinner("Thinking..."):
            reply = get_llm_response(user_query.strip())
        st.sidebar.markdown(f"**AI Response:**\n\n{reply}")
    else:
        st.sidebar.warning("⚠️ Please enter a question before submitting.")

# Main Dashboard section
st.subheader("📊 Demand Forecast Dashboard")
st.markdown("*(Your ML model outputs and visualizations go here)*")

# Example placeholder chart
st.line_chart({
    "Whiskey": [120, 135, 150, 170],
    "Wine": [80, 95, 110, 130],
    "Beer": [200, 220, 250, 270]
})
