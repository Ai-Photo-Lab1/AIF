# -*- coding: utf-8 -*-
import streamlit as st
from openai import OpenAI
import io

# 1. Page Configuration (Light Gemini/ChatGPT Theme)
st.set_page_config(
    page_title="AIF - Next Gen AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for Clean White Gemini/ChatGPT Theme
st.markdown("""
    <style>
    /* Global Light Background */
    .stApp {
        background-color: #ffffff;
        color: #1f2937;
    }
    
    /* Main Header Styling */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e293b;
        text-align: center;
        margin-top: 10px;
    }
    
    .main-subtitle {
        font-size: 1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    /* New Chat Button */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #0f172a;
        color: #ffffff;
        border: none;
        font-weight: 600;
        padding: 10px 16px;
    }
    .stButton>button:hover {
        background-color: #334155;
        color: #ffffff;
    }

    /* Chat History Sidebar Buttons */
    .history-btn button {
        background-color: transparent !important;
        color: #334155 !important;
        border: 1px solid #e2e8f0 !important;
        text-align: left !important;
        font-weight: 400 !important;
        margin-bottom: 5px;
    }
    .history-btn button:hover {
        background-color: #f1f5f9 !important;
        border-color: #cbd5e1 !important;
    }

    /* Footer Slogan */
    .footer-text {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #ffffff;
        color: #64748b;
        text-align: center;
        font-size: 0.85rem;
        padding: 8px 0;
        border-top: 1px solid #f1f5f9;
        z-index: 100;
    }

    /* Chat Messages */
    [data-testid="stChatMessage"] {
        background-color: #f8fafc;
        border-radius: 16px;
        padding: 14px 18px;
        margin-bottom: 12px;
        border: 1px solid #f1f5f9;
    }
    </style>
""", unsafe_allow_html=True)

# 3. API Key Configuration
import os

API_KEY = os.environ.get(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)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

# 4. Smart System Prompt (Auto-Correction & High Intelligence)
SYSTEM_PROMPT = """
You are AIF (AI Is in the Future), an advanced, highly intelligent multimodal AI assistant.

CRITICAL INSTRUCTIONS FOR BEHAVIOR:
1. SMART TYPO CORRECTION: The user may have typos, spelling errors, or casual slang in their prompts. Always understand the true intent, ignore minor typos silently, and answer accurately without pointing out the typos.
2. CREATOR DISCLOSURE: Only if directly and explicitly asked "who made you" or "who created you", answer that you were created by "Sayyed Amir Hamza Sadat" (سید امیر حمزه سادات). Do not mention age or extra details unless asked.
3. BEHAVIOR: Be dynamic, extremely helpful, natural, and friendly—exactly like ChatGPT or Gemini.
4. POLYGLOT: Respond naturally in whatever language the user talks to you in.
"""

# 5. Helper Function to Read File Content (Built-in text reader)
def get_file_content(uploaded_file):
    try:
        return io.StringIO(uploaded_file.getvalue().decode("utf-8")).read()
    except Exception:
        return f"[File Attached: {uploaded_file.name}]"

# 6. Session State Management for Multi-Chat Memory
if "chats" not in st.session_state:
    st.session_state["chats"] = {}

if "current_chat_id" not in st.session_state:
    st.session_state["current_chat_id"] = None

def create_new_chat():
    new_id = f"chat_{len(st.session_state['chats']) + 1}"
    st.session_state["chats"][new_id] = {
        "title": "New Conversation",
        "messages": []
    }
    st.session_state["current_chat_id"] = new_id

if not st.session_state["chats"] or st.session_state["current_chat_id"] is None:
    create_new_chat()

# 7. Sidebar
with st.sidebar:
    st.markdown("### ✨ AIF Workspace")
    
    if st.button("➕ New Chat"):
        create_new_chat()
        st.rerun()

    st.divider()
    
    search_query = st.text_input("🔍 Search Chats", placeholder="Filter history...")
    
    st.markdown("#### 🕒 Recent Chats")
    
    for cid, cdata in list(st.session_state["chats"].items()):
        title = cdata["title"]
        if search_query and search_query.lower() not in title.lower():
            continue
            
        label = f"💬 {title[:22]}..." if len(title) > 22 else f"💬 {title}"
        st.markdown("<div class='history-btn'>", unsafe_allow_html=True)
        if st.button(label, key=cid):
            st.session_state["current_chat_id"] = cid
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# 8. Main Content Header
st.markdown("<div class='main-title'>✨ AIF</div>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Developed & Powered by Sayyed Amir Hamza Sadat</div>", unsafe_allow_html=True)

current_chat = st.session_state["chats"][st.session_state["current_chat_id"]]

# 9. Render Messages
for msg in current_chat["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 10. File & Voice Controls
col1, col2 = st.columns([1, 1])
with col1:
    uploaded_file = st.file_uploader("📷 Attach File / Image", type=["jpg", "png", "jpeg", "mp4", "txt"], label_visibility="collapsed")
    if uploaded_file:
        st.toast(f"Attached: {uploaded_file.name}")

with col2:
    audio_file = st.audio_input("🎙️ Voice Input", label_visibility="collapsed")
    if audio_file:
        st.toast("Voice captured!")

# 11. User Input & Processing
if prompt := st.chat_input("Ask AIF anything..."):
    if len(current_chat["messages"]) == 0:
        current_chat["title"] = prompt[:30]

    file_context = ""
    if uploaded_file is not None:
        extracted = get_file_content(uploaded_file)
        file_context = f"\n\n[Attached File Content ({uploaded_file.name}):]\n{extracted}"

    current_chat["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in current_chat["messages"]:
        if m == current_chat["messages"][-1] and file_context:
            api_messages.append({"role": "user", "content": prompt + file_context})
        else:
            api_messages.append({"role": m["role"], "content": m["content"]})

    with st.chat_message("assistant"):
        with st.spinner("⚡ AIF is thinking..."):
            try:
                completion = client.chat.completions.create(
                    model="openrouter/free",
                    messages=api_messages,
                    temperature=0.7,
                )
                response = completion.choices[0].message.content
            except Exception as e:
                response = f"Error: {e}"
        st.write(response)

    current_chat["messages"].append({"role": "assistant", "content": response})

# 12. Fixed Footer Slogan
st.markdown("<div class='footer-text'>Where human vision meets ultimate intelligence.</div>", unsafe_allow_html=True)