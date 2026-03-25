import streamlit as st
import requests
import json
import os

FILE_NAME = "chats.json"

def load_chats():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return {}

def save_chats(chats):
    with open(FILE_NAME, "w") as f:
        json.dump(chats, f)
# 🔐 API Key
API_KEY = st.secrets["GEMINI_API_KEY"]

# 🌐 Config
st.set_page_config(page_title="Billa", page_icon="🌐", layout="wide")

# 🧠 Initialize session state
if "chats" not in st.session_state:
    st.session_state.chats = load_chats()

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

    # 📜 Chat list with ⋮ menu
    for chat in list(st.session_state.chats.keys()):
        col1, col2 = st.columns([6, 1])

        # 📂 Open chat
        with col1:
            if st.button(chat, key=f"open_{chat}"):
                st.session_state.current_chat = chat

        # ⋮ Menu
        with col2:
            with st.popover("⋮"):

                # ✏️ Rename
                if st.button("✏️ Rename", key=f"rename_{chat}"):
                    st.session_state.rename_chat = chat

                # 🗑️ Delete
                if st.button("🗑️ Delete", key=f"delete_{chat}"):
                    del st.session_state.chats[chat]

                    # Reset current chat if deleted
                    if st.session_state.current_chat == chat:
                        st.session_state.current_chat = None

                    st.rerun()

# 🏷️ Title + Clear button
col1, col2 = st.columns([6,1])

with col1:
    st.title("🤖 Billa AI Assistant")
    st.caption("Hi, I'm Billa 👋 Ask me anything!")

with col2:
    if st.session_state.current_chat:
        if st.button("🧹 Clear Chat"):
            st.session_state.chats[st.session_state.current_chat] = []
            st.rerun()

# ⚠️ No chat selected
if not st.session_state.current_chat:
    st.info("Create a new chat to start 🚀")
    st.stop()

# 📂 Current chat
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

if st.button("🚀 Send") and query:

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

    # Save
    st.session_state.chats[st.session_state.current_chat] = messages

    st.rerun()
