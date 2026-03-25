import streamlit as st
import requests

# 🔐 Load API Key
API_KEY = st.secrets["GEMINI_API_KEY"]

# 🌐 Page Config
st.set_page_config(page_title="Billa AI", page_icon="🌐", layout="wide")

# 🧠 Initialize memory
if "permanent_history" not in st.session_state:
    st.session_state.permanent_history = []

# 🤖 Gemini API function
def ask_gemini(messages):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={API_KEY}"

    contents = []

    # 🧠 Billa personality
    contents.append({
        "parts": [{
            "text": "You are Billa, a smart, friendly AI assistant like Siri. Keep answers clear, helpful, and slightly conversational."
        }]
    })

    for role, msg in messages:
        contents.append({
            "parts": [{"text": f"{role}: {msg}"}]
        })

    response = requests.post(url, json={"contents": contents})
    return response.json()

# 🎯 SIDEBAR
with st.sidebar:
    st.title("💬 Billa")

    chat_mode = st.radio(
        "Choose Mode",
        ["🟢 Permanent Chat", "⚡ Temporary Chat"]
    )

    st.markdown("---")

    if st.button("🧹 Clear Permanent Chat"):
        st.session_state.permanent_history = []

    st.markdown("---")

    # 🔎 Search Panel
    st.markdown("### 🔎 Search")
    search_query = st.text_input("Search the web")

    if search_query:
        st.markdown(f"[👉 Search on DuckDuckGo](https://duckduckgo.com/?q={search_query})")

# 🏷️ Main Title
st.title("🤖 Billa - Your AI Assistant")
st.caption("Hi, I'm Billa 👋 Ask me anything!")

# 💬 Input Area
col1, col2 = st.columns([8,1])

with col1:
    query = st.text_input("Talk to Billa...")

with col2:
    send = st.button("🚀")

# 📩 Handle Query
if send and query:

    if chat_mode == "🟢 Permanent Chat":
        st.session_state.permanent_history.append(("You", query))
        messages = st.session_state.permanent_history
    else:
        messages = [("You", query)]

    with st.spinner("Billa is thinking... 🤔"):
        result = ask_gemini(messages)

        if "error" in result:
            answer = "⚠️ Billa is busy right now. Try again later."
        else:
            try:
                answer = result["candidates"][0]["content"]["parts"][0]["text"]
            except:
                answer = "⚠️ Error understanding response."

    if chat_mode == "🟢 Permanent Chat":
        st.session_state.permanent_history.append(("Billa", answer))

# 🧾 Display Chat
if chat_mode == "🟢 Permanent Chat":
    history = st.session_state.permanent_history
else:
    history = []

for role, msg in history:
    if role == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 Billa:** {msg}")
    st.write("---")
