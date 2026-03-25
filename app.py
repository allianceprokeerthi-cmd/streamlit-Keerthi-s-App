import streamlit as st
import requests

# Load API key
API_KEY = st.secrets["GEMINI_API_KEY"]

st.set_page_config(page_title="AI Search", page_icon="🤖")

st.title("PSK Search Engine 🤖")

query = st.text_input("Ask anything...")

def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
    
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(url, json=data)
    return response.json()

if st.button("Search") and query:
    with st.spinner("Thinking... 🤔"):
        result = ask_gemini(query)

        try:
            answer = result["candidates"][0]["content"]["parts"][0]["text"]
            st.subheader("Answer")
            st.write(answer)
        except:
            st.error("Error getting response")
            st.write(result)
