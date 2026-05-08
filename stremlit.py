import streamlit as st
import requests
import uuid

st.set_page_config(
    page_title="OpenEyes Technology Agent",
    page_icon="🤖",
    layout="centered",
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_mode" not in st.session_state:
    st.session_state.agent_mode = False
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

agent_mode = st.session_state.agent_mode

if agent_mode:
    bg         = "#0f0f0f"
    text       = "#e5e5e5"
    user_bg    = "#1e3a8a"
    bot_bg     = "#1a1a1a"
    border     = "#2a2a2a"
    accent     = "#7a9cff"
    sub_color  = "#888"
else:
    bg         = "#ffffff"
    text       = "#111111"
    user_bg    = "#4a6cf7"
    bot_bg     = "#f4f4f5"
    border     = "#e5e5e5"
    accent     = "#4a6cf7"
    sub_color  = "#888"

st.markdown(f"""
<style>
  html, body, [class*="css"] {{
    background-color: {bg} !important;
    color: {text} !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }}
  .stApp {{ background-color: {bg} !important; }}
  #MainMenu, footer, header {{ display: none !important; }}
  .block-container {{ max-width: 680px; padding: 1.5rem 1rem 5rem; margin: auto; }}

  h1 {{
    color: {accent} !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    text-align: center;
    letter-spacing: -0.02em;
  }}

  .user-msg {{
    background: {user_bg};
    color: #ffffff;
    padding: 8px 12px;
    border-radius: 14px 14px 3px 14px;
    margin: 4px 0 4px auto;
    max-width: 72%;
    width: fit-content;
    font-size: 0.875rem;
    line-height: 1.5;
  }}
  .bot-msg {{
    background: {bot_bg};
    color: {text};
    padding: 8px 12px;
    border-radius: 14px 14px 14px 3px;
    margin: 4px auto 4px 0;
    max-width: 72%;
    width: fit-content;
    font-size: 0.875rem;
    line-height: 1.5;
    border: 0.5px solid {border};
  }}

  [data-testid="stChatInput"] textarea {{
    background: {bot_bg} !important;
    color: {text} !important;
    border: 0.5px solid {border} !important;
    border-radius: 10px !important;
    font-size: 0.875rem !important;
  }}
  [data-testid="stChatInput"] textarea:focus {{
    border-color: {accent} !important;
  }}
  [data-testid="stChatInput"] {{ background: {bg} !important; }}

  [data-testid="stToggle"] > label > div[data-testid="stMarkdownContainer"] p {{
    color: {accent} !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
  }}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"<h1>OpenEyes Technology Agent</h1>", unsafe_allow_html=True)
st.markdown(
    f"<p style='text-align:center;font-size:11px;letter-spacing:0.1em;color:{sub_color};text-transform:uppercase;margin-top:-0.5rem;'>AI Powered Multi-Agent Assistant</p>",
    unsafe_allow_html=True,
)
if agent_mode:
    st.markdown(
        f"<p style='text-align:center;font-size:12px;color:{accent};margin-top:-0.25rem;'>🧠 Agent Mode Activated</p>",
        unsafe_allow_html=True,
    )

st.write("")

# ── Toggle ────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 2, 2])
with col1:
    st.markdown(f"<p style='text-align:right;line-height:2rem;font-size:13px;font-weight:500;color:{accent};'>Normal Chat</p>", unsafe_allow_html=True)
with col2:
    new_mode = st.toggle("Agent Mode", value=agent_mode, label_visibility="collapsed")
with col3:
    st.markdown(f"<p style='line-height:2rem;font-size:13px;font-weight:500;color:{''+accent+'' if agent_mode else '#aaa'};'>Agent Mode</p>", unsafe_allow_html=True)

if new_mode != agent_mode:
    st.session_state.agent_mode = new_mode
    st.rerun()

st.divider()

# ── Messages ──────────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    css = "user-msg" if msg["role"] == "user" else "bot-msg"
    st.markdown(f'<div class="{css}">{msg["content"]}</div>', unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
prompt = st.chat_input("Type a message…")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    # ──────────────────────────────────────────────────────────────────────────
    # 🔌 API INTEGRATION — replace get_ai_response() body with your API call
    # ──────────────────────────────────────────────────────────────────────────
    def get_ai_response(user_message: str) -> str:
        api_url = st.secrets.get("API_URL", "http://127.0.0.1:8000")
        mode = "agent" if st.session_state.agent_mode else "normal"
        try:
            resp = requests.post(
                f"{api_url}/chat",
                json={
                    "message": user_message,
                    "mode": mode,
                    "session_id": st.session_state.session_id,
                },
                timeout=120,
            )
            resp.raise_for_status()
            return resp.json().get("reply", "")
        except Exception as exc:
            return f"API error: {exc}"

    reply = get_ai_response(prompt)
    st.session_state.messages.append({"role": "bot", "content": reply})
    st.rerun()