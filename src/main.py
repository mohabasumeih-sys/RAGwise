import streamlit as st
import sys
import os

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from chatbot_utility import ask, COLLECTIONS
from get_youtube_video import get_video_references

st.set_page_config(page_title="RAGwise", page_icon="📚", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=JetBrains+Mono:wght@400;500&family=Inter:wght@300;400;500&display=swap');

/* ── ROOT ── */
html, body, [class*="css"] {
    background-color: #080808 !important;
    color: #e8e0d8 !important;
    font-family: 'Inter', sans-serif !important;
}
.main { background-color: #080808 !important; }
.block-container {
    padding: 2.5rem 1.5rem 0 1.5rem !important;
    max-width: 100% !important;
    overflow: visible !important;
}
section[data-testid="stSidebar"] { display: none; }

/* ── HEADER ── */
.rag-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.3rem;
    overflow: visible;
    padding-top: 0.5rem;
}
.rag-logo {
    width: 42px; height: 42px;
    background: linear-gradient(135deg, #8b0000, #c0392b);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
}
.rag-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff !important;
    letter-spacing: -0.02em;
    line-height: 1;
    white-space: nowrap;
    display: block;
}
.rag-title span { color: #c0392b; }
.rag-sub {
    font-size: 0.8rem;
    color: #4a4040;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 1.4rem;
}

/* ── BOOK SELECTOR ── */
.stSelectbox > div > div {
    background: #111111 !important;
    border: 1px solid #2a1515 !important;
    border-radius: 10px !important;
    color: #e8e0d8 !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #8b0000 !important;
    box-shadow: 0 0 0 3px rgba(139,0,0,0.18) !important;
}
.stSelectbox label {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #8b0000 !important;
}
div[data-baseweb="select"] * { color: #e8e0d8 !important; }
div[data-baseweb="popover"] {
    background: #111111 !important;
    border: 1px solid #2a1515 !important;
}
li[role="option"]:hover { background: #1e0a0a !important; }

/* ── CHAT WINDOW ── */
.chat-wrap {
    background: #0d0d0d;
    border: 1px solid #1e0a0a;
    border-radius: 14px;
    height: 430px;
    overflow-y: auto;
    padding: 1.2rem 1.2rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 0.8rem;
    scrollbar-width: thin;
    scrollbar-color: #2a1515 transparent;
}
.chat-wrap::-webkit-scrollbar { width: 4px; }
.chat-wrap::-webkit-scrollbar-thumb { background: #2a1515; border-radius: 4px; }

.empty-state {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    height: 100%; gap: 0.6rem; color: #2a2020;
}
.empty-icon { font-size: 2.5rem; }
.empty-text { font-size: 0.85rem; letter-spacing: 0.06em; text-transform: uppercase; }

/* User bubble */
.bubble-user {
    background: #1a0a0a;
    border: 1px solid #2a1515;
    border-radius: 16px 16px 4px 16px;
    padding: 0.7rem 1rem;
    color: #e8e0d8;
    font-size: 0.88rem;
    max-width: 72%;
    align-self: flex-end;
    margin-left: auto;
    line-height: 1.5;
}

/* Bot bubble */
.bubble-bot-wrap { display: flex; flex-direction: column; gap: 0.3rem; max-width: 88%; }
.bubble-tag {
    font-size: 0.65rem;
    color: #8b0000;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    display: flex; align-items: center; gap: 5px;
}
.bubble-tag::before {
    content: '';
    display: inline-block;
    width: 6px; height: 6px;
    background: #8b0000;
    border-radius: 50%;
}
.bubble-bot {
    background: #111111;
    border: 1px solid #1e0a0a;
    border-left: 3px solid #8b0000;
    border-radius: 4px 16px 16px 16px;
    padding: 0.8rem 1rem;
    color: #ffffff;
    font-size: 0.9rem;
    line-height: 1.7;
}

/* ── INPUT ROW ── */
.stTextInput input {
    background: #111111 !important;
    border: 1px solid #2a1515 !important;
    border-radius: 10px !important;
    color: #e8e0d8 !important;
    font-size: 0.9rem !important;
    padding: 0.65rem 1rem !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput input::placeholder { color: #3a2525 !important; }
.stTextInput input:focus {
    border-color: #8b0000 !important;
    box-shadow: 0 0 0 3px rgba(139,0,0,0.15) !important;
    outline: none !important;
}
.stTextInput label { display: none !important; }

/* ── BUTTONS ── */
div[data-testid="stFormSubmitButton"] button,
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #8b0000, #a31515) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.6rem 0.8rem !important;
    width: 100% !important;
    transition: opacity 0.15s !important;
}
div[data-testid="stFormSubmitButton"] button:hover,
div[data-testid="stButton"] button:hover { opacity: 0.82 !important; }

/* ── RIGHT PANEL ── */
.panel-section { margin-bottom: 1.4rem; }
.panel-heading {
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #ff4444;
    margin-bottom: 0.7rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #2a1515;
    display: flex; align-items: center; gap: 6px;
}

.src-card {
    background: #0d0d0d;
    border: 1px solid #2a1515;
    border-left: 3px solid #c0392b;
    border-radius: 0 8px 8px 0;
    padding: 0.7rem 0.9rem;
    margin: 0.4rem 0;
    font-size: 0.82rem;
}
.src-name { color: #ff6b6b; font-weight: 700; font-size: 0.88rem; margin-bottom: 0.2rem; }
.src-meta { color: #cccccc; font-size: 0.78rem; margin: 0.2rem 0; }
.src-snippet { color: #ffffff; font-style: italic; font-size: 0.78rem; line-height: 1.5; margin-top: 0.25rem; }
.src-score {
    display: inline-block;
    background: #2a0808;
    color: #ff6b6b;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    padding: 2px 7px;
    border-radius: 4px;
    border: 1px solid #4a1515;
    font-weight: 600;
}

.yt-card {
    background: #0d0d0d;
    border: 1px solid #1e0a0a;
    border-radius: 10px;
    overflow: hidden;
    margin: 0.4rem 0;
}
.yt-card:hover { border-color: #8b0000; }
.yt-thumb { width: 100%; height: 90px; object-fit: cover; display: block; }
.yt-body { padding: 0.55rem 0.7rem; }
.yt-title { color: #ffffff; font-size: 0.82rem; font-weight: 600; line-height: 1.4; margin-bottom: 0.2rem; }
.yt-meta { color: #aaaaaa; font-size: 0.72rem; margin-bottom: 0.35rem; }
.yt-btn {
    display: inline-flex; align-items: center; gap: 4px;
    background: #1a0808;
    color: #c0392b !important;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 5px;
    border: 1px solid #2a1515;
    text-decoration: none !important;
    letter-spacing: 0.04em;
}
.yt-btn:hover { background: #2a1010; border-color: #8b0000; }

.placeholder {
    color: #555555;
    font-size: 0.82rem;
    text-align: center;
    padding: 1.2rem 0;
    font-style: italic;
}

/* Spinner */
.stSpinner > div { border-top-color: #8b0000 !important; }

/* Divider */
hr { border-color: #1e0a0a !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── LAYOUT ───────────────────────────────────────────────────────────────────
left, right = st.columns([13, 7], gap="large")

# ══════════════════════════════════════════
# LEFT — Chat
# ══════════════════════════════════════════
with left:
    st.markdown("""
    <div class="rag-header">
        <div class="rag-logo">📚</div>
        <div class="rag-title">RAG<span>wise</span></div>
    </div>
    <div class="rag-sub">AI · ML · Deep Learning · NLP · LLM</div>
    """, unsafe_allow_html=True)

    book_options  = list(COLLECTIONS.keys())
    selected_book = st.selectbox("Select Book", options=book_options, index=0)

    # Chat window
    bubbles = ""
    if not st.session_state.history:
        bubbles = """
        <div class="empty-state">
            <div class="empty-icon">💬</div>
            <div class="empty-text">Ask a question to begin</div>
        </div>"""
    else:
        for entry in st.session_state.history:
            bubbles += f'<div class="bubble-user">{entry["question"]}</div>'
            bubbles += f"""
            <div class="bubble-bot-wrap">
                <div class="bubble-tag">RAGwise · {entry["book"]}</div>
                <div class="bubble-bot">{entry["answer"]}</div>
            </div>"""

    st.markdown(f"""
    <div class="chat-wrap" id="ragchat">{bubbles}</div>
    <script>
        const c = document.getElementById('ragchat');
        if (c) c.scrollTop = c.scrollHeight;
    </script>
    """, unsafe_allow_html=True)

    # Input form
    with st.form("qform", clear_on_submit=True):
        c1, c2 = st.columns([6, 1], gap="small")
        with c1:
            q = st.text_input("q", placeholder="Ask anything about the selected book...", label_visibility="collapsed")
        with c2:
            go = st.form_submit_button("Ask →")

    if st.session_state.history:
        if st.button("✕ Clear conversation"):
            st.session_state.history = []
            st.rerun()

    # Process
    if go and q.strip():
        with st.spinner("Searching and generating answer..."):
            result   = ask(q, book_label=selected_book)
            col_key  = COLLECTIONS.get(selected_book, "all")
            videos   = get_video_references(q, collection_name=col_key)

        st.session_state.history.append({
            "question": q,
            "answer":   result["answer"],
            "book":     selected_book,
            "sources":  result["sources"],
            "videos":   videos,
        })
        st.rerun()

# ══════════════════════════════════════════
# RIGHT — Sources + YouTube
# ══════════════════════════════════════════
with right:
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    if st.session_state.history:
        latest = st.session_state.history[-1]

        # Sources
        st.markdown('<div class="panel-heading">📄 Sources</div>', unsafe_allow_html=True)
        sources = latest.get("sources", [])
        if sources:
            for s in sources:
                snippet = s["snippet"][:130].replace('"', '&quot;')
                st.markdown(f"""
                <div class="src-card">
                    <div class="src-name">{s['file']}</div>
                    <div class="src-meta">
                        Page {s['page']} &nbsp;·&nbsp;
                        <span style="color:#4a3030">{s['collection']}</span>
                        &nbsp;·&nbsp; <span class="src-score">{s['score']}</span>
                    </div>
                    <div class="src-snippet">"{snippet}..."</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="placeholder">No sources found</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # YouTube
        st.markdown('<div class="panel-heading">▶ YouTube References</div>', unsafe_allow_html=True)
        videos = latest.get("videos", [])
        if videos:
            for v in videos:
                thumb_html = f'<img class="yt-thumb" src="{v["thumbnail"]}" />' if v.get("thumbnail") else ""
                title = v["title"].replace("<","&lt;").replace(">","&gt;")
                st.markdown(f"""
                <div class="yt-card">
                    {thumb_html}
                    <div class="yt-body">
                        <div class="yt-title">{title}</div>
                        <div class="yt-meta">{v['channel']} · {v['duration']} · {v['views']} views</div>
                        <a class="yt-btn" href="{v['url']}" target="_blank">▶ Watch</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="placeholder">No videos found</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="panel-heading">📄 Sources</div>', unsafe_allow_html=True)
        st.markdown('<div class="placeholder">Sources appear after your first question</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="panel-heading">▶ YouTube References</div>', unsafe_allow_html=True)
        st.markdown('<div class="placeholder">Videos appear after your first question</div>', unsafe_allow_html=True)