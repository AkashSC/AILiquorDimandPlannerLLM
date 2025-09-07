import os
import json
import requests
import pandas as pd
import streamlit as st
from prophet import Prophet

# -----------------------------
# LLM Response Function (Groq)
# -----------------------------
def get_llm_response(prompt: str, data_summary: str = "") -> str:
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

    # Combine query + dataset context
    full_prompt = f"""
    You are an AI advisor for liquor demand planning.
    Use the dataset summary and forecast data below to answer the question.

    Dataset summary:
    {data_summary}

    Question:
    {clean_prompt}
    """

    payload = {
        "model": "llama-3.1-8b-instant",  # ✅ supported Groq model
        "messages": [
            {"role": "system", "content": "You are a helpful AI advisor for liquor demand forecasting."},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
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
st.title("🍷 Liquor Demand Planner with AI + ML Forecast")

# Load dataset
df = pd.read_csv("liquor_sales.csv")

st.subheader("📊 Historical Sales Data")
st.dataframe(df)

# -----------------------------
# Prophet Forecast
# -----------------------------
st.subheader("🔮 Forecasting with Prophet")

# Prepare data for Prophet (Wine example, can loop for others)
df_wine = df[["Month", "Wine"]].copy()
df_wine["ds"] = pd.date_range(start="2023-01-01", periods=len(df_wine), freq="M")
df_wine["y"] = df_wine["Wine"]

model = Prophet()
model.fit(df_wine[["ds", "y"]])

future = model.make_future_dataframe(periods=3, freq="M")
forecast = model.predict(future)

# Show forecast dataframe
st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(5))

# Visualization
st.line_chart({
    "Historical": list(df_wine["y"]) + [None] * 3,
    "Forecast": list(forecast["yhat"])
})

# -----------------------------
# AI Advisor Section
# -----------------------------
st.sidebar.header("🔍 Ask the AI")
user_query = st.sidebar.text_area(
    "Type your question (e.g., demand trends, inventory tips, seasonal forecasts):",
    placeholder="Example: Forecast wine sales in December"
)

if st.sidebar.button("Get AI Advice"):
    if user_query.strip():
        with st.spinner("Thinking..."):
            # Pass dataset + forecast summary
            forecast_summary = forecast.tail(3)[["ds", "yhat"]].to_string(index=False)
            data_summary = df.describe().to_string()

            reply = get_llm_response(
                f"{user_query.strip()}\n\nHere are forecasted values:\n{forecast_summary}",
                data_summary
            )
        st.sidebar.markdown(f"**AI Response:**\n\n{reply}")
    else:
        st.sidebar.warning("⚠️ Please enter a question before submitting.")
