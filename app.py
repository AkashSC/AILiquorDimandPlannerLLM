import requests
import streamlit as st

# ---------------------------
# LLM Function
# ---------------------------
def get_llm_response(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",  # or "mistral-7b-8192"
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Liquor Demand Planner", layout="wide")
st.title("🍷 Liquor Demand Planner with AI Assistant")

# Sidebar - AI Assistant
st.sidebar.header("🔍 Ask the AI")
user_query = st.sidebar.text_input(
    "Type your question (e.g., demand trends, inventory tips):"
)

if user_query:
    with st.spinner("Thinking..."):
        reply = get_llm_response(user_query)
    st.sidebar.markdown(f"**AI Response:**\n\n{reply}")

# Main Dashboard
st.subheader("📊 Demand Forecast Dashboard")
st.markdown("*(Your ML model outputs and visualizations go here)*")

# Example placeholder chart
st.line_chart({
    "Whiskey": [120, 135, 150],
    "Wine": [80, 95, 110]
})
