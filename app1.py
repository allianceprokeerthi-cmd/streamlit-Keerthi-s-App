import streamlit as st
import requests

# 🔐 Load API key
API_KEY = st.secrets["GEMINI_API_KEY"]

# 🌐 Page config
st.set_page_config(page_title="AI Chat", page_icon="🤖", layout="wide")

# 🎨 Custom styling
st.markdown("""
    <style>
    .user-msg {
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
    }
    .bot-msg {
        background-color: #F1F0F0;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 🧠 Initialize chat memory
if "history" not in st.session_state:
    st.session_state.history = []

# 🤖 Gemini function
def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={API_KEY}"
    
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(url, json=data)
    return response.json()

# 🏷️ Title
st.title("🤖 AI Chat Assistant")

# 💬 Input box
col1, col2 = st.columns([8,1])

with col1:
    query = st.text_input("Ask anything...", key="input")

with col2:
    send = st.button("🚀")

# 📩 When user sends message
if send and query:

    # Add user message
    st.session_state.history.append(("user", query))

    with st.spinner("Thinking... 🤔"):
        result = ask_gemini(query)

        if "error" in result:
            answer = "⚠️ AI is busy. Please try again later."
        else:
            try:
                answer = result["candidates"][0]["content"]["parts"][0]["text"]
            except:
                answer = "⚠️ Error processing response."

    # Add AI response
    st.session_state.history.append(("bot", answer))

# 🧾 Display chat history
for role, message in st.session_state.history:
    if role == "user":
        st.markdown(f'<div class="user-msg"><b>🧑 You:</b> {message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg"><b>🤖 AI:</b> {message}</div>', unsafe_allow_html=True)

# 🧹 Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.history = []
