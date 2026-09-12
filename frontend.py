import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Enterprise Multi-PDF RAG Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* =======================
   GLOBAL
======================= */

html, body, [class*="css"]{
    font-size:12px !important;
}

.stApp{
    background:#F5F7FB;
}

/* Reduce page padding */

.block-container{
    padding-top:1rem;
    padding-left:2rem;
    padding-right:2rem;
    padding-bottom:1rem;
}

/* Hide Streamlit branding */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

/* =======================
   TITLE
======================= */

.main-title{
    font-size:30px;
    font-weight:700;
    color:#2563EB;
    margin-bottom:0px;
}

.sub-title{
    color:#6B7280;
    font-size:13px;
    margin-bottom:15px;
}

/* =======================
   HEADINGS
======================= */

h1{
    font-size:28px !important;
}

h2{
    font-size:20px !important;
}

h3{
    font-size:17px !important;
}

h4{
    font-size:15px !important;
}

/* =======================
   TEXT
======================= */

p,
span,
label,
div{
    font-size:12px !important;
}

/* =======================
   SIDEBAR
======================= */

section[data-testid="stSidebar"]{
    background:#FFFFFF;
    border-right:1px solid #E5E7EB;
}

section[data-testid="stSidebar"] *{
    font-size:12px !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{
    font-size:15px !important;
}

/* =======================
   METRICS
======================= */

[data-testid="stMetric"]{
    background:white;
    border-radius:12px;
    padding:15px;
    box-shadow:0 2px 8px rgba(0,0,0,.08);
}

[data-testid="stMetricValue"]{
    font-size:20px !important;
    font-weight:700;
}

[data-testid="stMetricLabel"]{
    font-size:11px !important;
}

/* =======================
   BUTTONS
======================= */

.stButton>button{
    width:100%;
    border-radius:10px;
    font-size:12px !important;
}

/* =======================
   CHAT
======================= */

.stChatInput input{
    font-size:12px !important;
}

[data-testid="stChatMessage"]{
    border-radius:12px;
    padding:10px;
    font-size:12px !important;
}

/* =======================
   SUCCESS / INFO BOXES
======================= */

.stAlert{
    font-size:12px !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

st.markdown("""
<div class='main-title'>
🤖 Enterprise Multi-PDF RAG Assistant
</div>

<div class='sub-title'>
Hybrid Retrieval • ChromaDB • BM25 • YOLO • OCR • CrossEncoder • Groq LLM
</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("📂 Knowledge Base")

    st.success("Machine Learning.pdf")
    st.success("Python.pdf")
    st.success("Deep Learning.pdf")

    st.divider()

    st.header("⚙ AI Pipeline")

    st.write("🔹 ChromaDB")
    st.write("🔹 BM25")
    st.write("🔹 YOLO")
    st.write("🔹 OCR")
    st.write("🔹 CrossEncoder")
    st.write("🔹 Groq LLM")

    st.divider()

    st.header("👨‍💻 Developer")

    st.write("**Devanshi Vyas**")
    st.caption("B.Tech CSE | AI & GenAI")

# ==========================================================
# DASHBOARD
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("📄 PDFs", "3")

with c2:
    st.metric("📑 Pages", "356")

with c3:
    st.metric("🖼 Images", "78")

with c4:
    st.metric("📊 Tables", "16")

st.divider()

# ==========================================================
# CHAT
# ==========================================================

question = st.chat_input("💬 Ask anything about your PDFs...")

if question:

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        st.write("⚡ Backend will answer here...")