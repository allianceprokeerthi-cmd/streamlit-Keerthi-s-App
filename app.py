import streamlit as st
import requests

# 🔐 API Key
API_KEY = st.secrets["GEMINI_API_KEY"]

# 🌐 Config
st.set_page_config(page_title="Billa", page_icon="🌐", layout="wide")

# 🧠 Initialize chats
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# 🤖 Gemini function
def ask_gemini(messages):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={API_KEY}"

    prompt = "You are Billa, a smart and friendly AI assistant.\n\n"

    for role, msg in messages:
        prompt += f"{role}: {msg}\n"

    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(url, json=data)
    return response.json()

# 🎯 SIDEBAR
with st.sidebar:
    st.title("💬 Billa")

    # ➕ New Chat
    if st.button("➕ New Chat"):
        chat_name = f"Chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[chat_name] = []
        st.session_state.current_chat = chat_name

    st.markdown("---")

    # 📜 Chat list
    for chat in st.session_state.chats:
        if st.button(chat):
            st.session_state.current_chat = chat

# 🏷️ Title
st.title("🤖 Billa - AI Assistant")
st.caption("Hi, I'm Billa 👋 Ask me anything!")
# ⚠️ No chat yet
if not st.session_state.current_chat:
    st.info("Create a new chat to start 🚀")
    st.stop()

# 📂 Current chat messages
messages = st.session_state.chats[st.session_state.current_chat]

# 💬 Display messages
for role, msg in messages:
    if role == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 Billa:** {msg}")
    st.write("---")

# 💬 Input
query = st.text_input("Ask Billa...")

if st.button("Start 🚀") and query:

    # Add user message
    messages.append(("You", query))

    with st.spinner("Billa thinking... 🤔"):
        result = ask_gemini(messages)

    if "error" in result:
        answer = result["error"]["message"]
    else:
        try:
            answer = result["candidates"][0]["content"]["parts"][0]["text"]
        except:
            answer = "⚠️ Error reading response"

    # Add AI response
    messages.append(("Billa", answer))

    # Save back
    st.session_state.chats[st.session_state.current_chat] = messages

    
# 🧹 Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.history = []

    # Refresh UI
    st.rerun()
