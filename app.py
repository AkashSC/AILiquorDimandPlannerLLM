import streamlit as st
from llm_utils import get_llm_response

st.set_page_config(page_title="Liquor Demand Planner", layout="wide")
st.title("🍷 Liquor Demand Planner with AI Assistant")

st.sidebar.header("🔍 Ask the AI")
user_query = st.sidebar.text_input("Type your question (e.g., demand trends, inventory tips):")

if user_query:
    with st.spinner("Thinking..."):
        reply = get_llm_response(user_query)
    st.sidebar.markdown(f"**AI Response:**\n\n{reply}")

st.subheader("📊 Demand Forecast Dashboard")
st.markdown("*(Your existing ML model outputs and visualizations go here)*")

# Example placeholder
st.line_chart({"Whiskey": [120, 135, 150], "Wine": [80, 95, 110]})
