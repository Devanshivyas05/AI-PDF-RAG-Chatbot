# # from src.rag_pipeline import RAGPipeline


# # def main():

# #     pdf_folder = "data"

# #     pipeline = RAGPipeline()

# #     pipeline.process_pdf(pdf_folder)

# #     while True:

# #         question = input("\nAsk your question (type 'exit' to quit): ")

# #         if question.lower() == "exit":
# #             print("\n👋 Thank you for using the Multi PDF RAG Chatbot!")
# #             break

# #         pipeline.ask(question)


# # if __name__ == "__main__":
# #     main()
# print("STEP 1")

# from src.rag_pipeline import RAGPipeline

# print("STEP 2")

# def main():
#     print("STEP 3")

#     pdf_folder = "data"

#     pipeline = RAGPipeline()

#     print("STEP 4")

#     pipeline.process_pdf(pdf_folder)

#     print("STEP 5")

#     while True:
#         question = input("Question: ")

#         if question == "exit":
#             break

#         pipeline.ask(question)

# if __name__ == "__main__":
#     print("STEP 6")
#     main()


import streamlit as st
from pathlib import Path

from src.rag_pipeline import RAGPipeline


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="RAGFlow | Multi-PDF Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
<style>

/* =========================================================
   GLOBAL
========================================================= */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(37, 99, 235, 0.10),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(124, 58, 237, 0.08),
            transparent 30%
        ),
        #0b1020;

    color: #e5e7eb;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.2rem;
    padding-bottom: 5rem;
    padding-left: 2rem;
    padding-right: 2rem;
}


/* =========================================================
   HIDE STREAMLIT DEFAULT UI
========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* =========================================================
   SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #1e293b;
}

section[data-testid="stSidebar"] * {
    color: #cbd5e1;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white;
}


/* =========================================================
   BRAND
========================================================= */

.brand {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 4px;
}

.brand-icon {
    width: 46px;
    height: 46px;
    border-radius: 14px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    );

    font-size: 24px;

    box-shadow:
        0 10px 30px rgba(37, 99, 235, 0.25);
}

.brand-title {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.8px;

    background: linear-gradient(
        90deg,
        #60a5fa,
        #a78bfa
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.brand-subtitle {
    color: #94a3b8;
    font-size: 12px;
    margin-left: 60px;
    margin-bottom: 22px;
}


/* =========================================================
   HERO
========================================================= */

.hero {
    padding: 28px;
    border-radius: 22px;

    background:
        linear-gradient(
            135deg,
            rgba(37, 99, 235, 0.15),
            rgba(124, 58, 237, 0.12)
        );

    border: 1px solid rgba(96, 165, 250, 0.18);

    box-shadow:
        0 20px 60px rgba(0, 0, 0, 0.25);

    margin-bottom: 22px;
}

.hero-title {
    font-size: 25px;
    font-weight: 700;
    color: white;
    margin-bottom: 8px;
}

.hero-text {
    font-size: 13px;
    color: #94a3b8;
    line-height: 1.7;
}


/* =========================================================
   STATUS
========================================================= */

.status {
    display: inline-flex;
    align-items: center;
    gap: 7px;

    padding: 6px 12px;

    border-radius: 999px;

    background: rgba(34, 197, 94, 0.10);

    border: 1px solid rgba(34, 197, 94, 0.25);

    color: #86efac;

    font-size: 11px;
    font-weight: 600;

    margin-bottom: 12px;
}


/* =========================================================
   METRICS
========================================================= */

[data-testid="stMetric"] {
    background: rgba(15, 23, 42, 0.78);

    border: 1px solid #1e293b;

    border-radius: 16px;

    padding: 14px 16px;

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.15);
}

[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    color: #94a3b8 !important;
}

[data-testid="stMetricValue"] {
    font-size: 22px !important;
    color: white !important;
    font-weight: 700 !important;
}


/* =========================================================
   CARDS
========================================================= */

.card {
    background: rgba(15, 23, 42, 0.72);

    border: 1px solid #1e293b;

    border-radius: 18px;

    padding: 20px;

    margin-top: 15px;

    box-shadow:
        0 10px 35px rgba(0, 0, 0, 0.15);
}

.card-title {
    font-size: 14px;
    font-weight: 700;
    color: white;
    margin-bottom: 10px;
}

.card-text {
    font-size: 12px;
    color: #94a3b8;
    line-height: 1.7;
}


/* =========================================================
   TECHNOLOGY BADGES
========================================================= */

.badge {
    display: inline-block;

    padding: 5px 9px;

    margin: 3px;

    border-radius: 8px;

    background: rgba(59, 130, 246, 0.10);

    border: 1px solid rgba(59, 130, 246, 0.18);

    color: #93c5fd;

    font-size: 10px;
}


/* =========================================================
   PDF ITEMS
========================================================= */

.pdf-item {
    padding: 10px 12px;

    margin: 6px 0;

    border-radius: 10px;

    background: #111827;

    border: 1px solid #1e293b;

    color: #cbd5e1;

    font-size: 11px;

    transition: all 0.2s ease;
}

.pdf-item:hover {
    border-color: #3b82f6;
    background: #172554;
}


/* =========================================================
   CHAT
========================================================= */

[data-testid="stChatMessage"] {
    background: rgba(15, 23, 42, 0.65);

    border: 1px solid #1e293b;

    border-radius: 16px;

    margin-bottom: 10px;
}

[data-testid="stChatMessage"] p {
    font-size: 13px !important;
    line-height: 1.7;
}


/* =========================================================
   CHAT INPUT
========================================================= */

[data-testid="stChatInput"] {
    background: #111827;
}

[data-testid="stChatInput"] textarea {
    font-size: 13px !important;
}


/* =========================================================
   BUTTONS
========================================================= */

.stButton > button {
    border-radius: 10px;

    border: 1px solid #334155;

    background: #111827;

    color: #cbd5e1;

    font-size: 12px;

    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #3b82f6;

    color: white;

    background: #172554;
}


/* =========================================================
   EXPANDER
========================================================= */

.streamlit-expanderHeader {
    font-size: 12px !important;
}


/* =========================================================
   SMALL TEXT
========================================================= */

.small-text {
    font-size: 10px;
    color: #64748b;
}

</style>
""",
    unsafe_allow_html=True
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================================
# LOAD RAG PIPELINE
# ==========================================================

@st.cache_resource(show_spinner=False)
def load_rag_pipeline():

    pipeline = RAGPipeline()

    data_folder = Path("data")

    if not data_folder.exists():
        raise FileNotFoundError(
            "The 'data' folder was not found."
        )

    pipeline.process_pdf(str(data_folder))

    return pipeline


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        """
<div style="
font-size:23px;
font-weight:800;
color:white;
margin-bottom:4px;
">
🧠 RAGFlow
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="small-text">
MULTI-PDF INTELLIGENCE SYSTEM
</div>
""",
        unsafe_allow_html=True
    )

    st.divider()


    # ------------------------------------------------------
    # KNOWLEDGE BASE
    # ------------------------------------------------------

    st.markdown("### 📚 Knowledge Base")

    data_path = Path("data")

    if data_path.exists():

        pdf_files = sorted(
            data_path.glob("*.pdf")
        )

        if pdf_files:

            for pdf in pdf_files:

                st.markdown(
                    f"""
<div class="pdf-item">
📄 {pdf.name}
</div>
""",
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "No PDF files found in data/"
            )

    else:

        st.warning(
            "data/ folder not found"
        )


    st.divider()


    # ------------------------------------------------------
    # AI PIPELINE
    # ------------------------------------------------------

    st.markdown("### ⚙️ AI Pipeline")

    technologies = [
        "BGE Embeddings",
        "ChromaDB",
        "BM25",
        "PDF Router",
        "CrossEncoder",
        "Groq LLM",
        "YOLO",
        "OCR",
        "Image Retriever",
        "Table Retriever",
        "Conversation Memory"
    ]

    for technology in technologies:

        st.markdown(
            f"""
<span class="badge">
◆ {technology}
</span>
""",
            unsafe_allow_html=True
        )


    st.divider()


    # ------------------------------------------------------
    # CONTROLS
    # ------------------------------------------------------

    st.markdown("### 🛠 Controls")

    if st.button(
        "🗑 Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


    st.divider()


    # ------------------------------------------------------
    # DEVELOPER
    # ------------------------------------------------------

    st.markdown(
        """
<div style="
color:#64748b;
font-size:10px;
line-height:1.7;
">

<b style="color:#94a3b8;">
Developer
</b>

<br>

Devanshi Vyas

<br>

B.Tech CSE • AI & GenAI

</div>
""",
        unsafe_allow_html=True
    )


# ==========================================================
# MAIN BRAND HEADER
# ==========================================================

st.markdown(
    """
<div class="brand">
<div class="brand-icon">🧠</div>
<div class="brand-title">RAGFlow</div>
</div>

<div class="brand-subtitle">
Enterprise Multi-PDF Intelligence Assistant
</div>
""",
    unsafe_allow_html=True
)


# ==========================================================
# HERO
# ==========================================================

st.markdown(
    """
<div class="hero">

<div class="status">
● AI KNOWLEDGE ENGINE
</div>

<div class="hero-title">
Ask your documents anything.
</div>

<div class="hero-text">
Search across your PDF knowledge base using hybrid retrieval,
semantic embeddings, BM25 ranking and CrossEncoder reranking —
then generate grounded answers using Groq LLM.
</div>

</div>
""",
    unsafe_allow_html=True
)


# ==========================================================
# DOCUMENT / SYSTEM STATS
# ==========================================================

data_path = Path("data")

if data_path.exists():

    pdf_files = list(
        data_path.glob("*.pdf")
    )

else:

    pdf_files = []


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "📄 Documents",
        len(pdf_files)
    )


with c2:

    st.metric(
        "🔎 Retrieval",
        "Hybrid"
    )


with c3:

    st.metric(
        "🧠 Embeddings",
        "BGE"
    )


with c4:

    st.metric(
        "⚡ LLM",
        "Groq"
    )


# ==========================================================
# INITIALIZE RAG PIPELINE
# ==========================================================

try:

    with st.spinner(
        "🚀 Initializing RAG knowledge engine..."
    ):

        pipeline = load_rag_pipeline()

except Exception as error:

    st.error(
        "⚠️ Unable to initialize the RAG pipeline."
    )

    with st.expander(
        "Technical details"
    ):

        st.code(
            str(error)
        )

    st.stop()


# ==========================================================
# READY CARD
# ==========================================================

st.markdown(
    """
<div class="card">

<div class="card-title">
🟢 Knowledge Base Ready
</div>

<div class="card-text">
Your PDF knowledge base is connected to the existing
RAG pipeline. Ask a question below to search,
retrieve and generate an answer.
</div>

</div>
""",
    unsafe_allow_html=True
)


# ==========================================================
# CHAT HISTORY
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ==========================================================
# CHAT INPUT
# ==========================================================

question = st.chat_input(
    "💬 Ask anything about your PDFs..."
)


if question:

    # ------------------------------------------------------
    # USER
    # ------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # ------------------------------------------------------
    # ASSISTANT
    # ------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🔎 Searching your knowledge base..."
        ):

            try:

                answer = pipeline.ask(
                    question
                )

                if answer is None:

                    answer = (
                        "I couldn't find a direct answer "
                        "for that query. Try asking more "
                        "specifically about the PDF content."
                    )

                elif not isinstance(
                    answer,
                    str
                ):

                    answer = str(answer)


            except Exception as error:

                answer = (
                    "⚠️ An error occurred while "
                    "processing your question."
                )

                with st.expander(
                    "Technical details"
                ):

                    st.code(
                        str(error)
                    )


        st.markdown(answer)

        st.caption(
            "Generated using the existing RAG pipeline • Groq LLM"
        )


    # ------------------------------------------------------
    # SAVE ASSISTANT RESPONSE
    # ------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# ==========================================================
# HOW THE SYSTEM WORKS
# ==========================================================

with st.expander(
    "🔬 How this RAG system works",
    expanded=False
):

    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            """
### 1️⃣ Document Processing

📄 PDF Loader

↓

✂️ Text Splitting

↓

🧠 BGE Embeddings

↓

🗄️ ChromaDB + BM25
"""
        )


    with col2:

        st.markdown(
            """
### 2️⃣ Retrieval

💬 User Query

↓

📂 PDF Router

↓

🔎 Hybrid Retrieval

↓

🎯 CrossEncoder Reranking
"""
        )


    with col3:

        st.markdown(
            """
### 3️⃣ Generation

📚 Retrieved Context

↓

🧠 Conversation Memory

↓

⚡ Groq LLM

↓

💬 Grounded Answer
"""
        )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    """
<div style="
text-align:center;
padding:25px 0 10px 0;
color:#475569;
font-size:10px;
">

RAGFlow • Multi-PDF Intelligence Platform

<br>

Built with Python • Streamlit • ChromaDB • BM25 • YOLO • OCR • Groq

</div>
""",
    unsafe_allow_html=True
)