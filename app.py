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
        if response.status_code == 400:
            return "⚠️ Bad Request: Please check your input."
        elif response.status_code == 401:
            return "❌ Unauthorized: Invalid or missing API key."
        elif response.status_code == 429:
            return "⏳ Rate limit exceeded. Please try again later."
        else:
            return f"❌ HTTP Error: {http_err}"

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
