import os
import requests
import streamlit as st

st.title("🔑 Groq API Key Test (Render)")

# Show whether key is available
api_key = os.environ.get("GROQ_API_KEY")
if api_key:
    st.success("✅ GROQ_API_KEY found in environment")
    st.write("Key starts with:", api_key[:6] + "******")
else:
    st.error("❌ GROQ_API_KEY not found in environment variables")

# Button to test actual Groq connectivity
if st.button("Test Groq API"):
    if not api_key:
        st.error("❌ No API key to test with.")
    else:
        try:
            r = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            r.raise_for_status()
            models = [m["id"] for m in r.json()["data"]]
            st.success("✅ Groq API works!")
            st.write("Available models:", models)
        except Exception as e:
            st.error(f"❌ API test failed: {e}")
