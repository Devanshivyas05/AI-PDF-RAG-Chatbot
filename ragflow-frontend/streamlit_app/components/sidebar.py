"""Sidebar: brand, knowledge base, stats, history, settings, pipeline status."""

from typing import Any, Callable, Dict, List

import streamlit as st

from components.document_card import document_card
from components.stats import stats_grid

PIPELINE = ["PDF Processing", "Hybrid Retrieval", "ChromaDB", "BM25", "YOLO", "OCR", "CrossEncoder", "Groq"]


def render_sidebar(
    documents: List[Dict[str, Any]],
    selected: List[str],
    stats: Dict[str, int],
    threads: List[Dict[str, Any]],
    backend_online: bool,
    on_toggle_doc: Callable[[str], None],
    on_delete_doc: Callable[[str], None],
    on_upload: Callable[[Any], None],
    on_new_chat: Callable[[], None],
    on_clear_chat: Callable[[], None],
) -> Dict[str, Any]:
    with st.sidebar:
        st.markdown(
            """
            <div class="brand">
              <div class="brand-mark">✦</div>
              <div>
                <div class="brand-name">Enterprise RAG</div>
                <div class="brand-sub">Multi-PDF Assistant</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        status = "ready" if backend_online else "error"
        label = "Backend connected" if backend_online else "Backend offline (mock mode)"
        st.markdown(
            f'<div class="chip"><span class="dot {status}"></span>{label}</div>',
            unsafe_allow_html=True,
        )

        if st.button("＋  New chat", use_container_width=True):
            on_new_chat()

        st.markdown('<div class="section-label">Knowledge base</div>', unsafe_allow_html=True)
        files = st.file_uploader(
            "Upload PDFs", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed"
        )
        if files:
            on_upload(files)

        if documents:
            for doc in documents:
                document_card(doc, doc["id"] in selected, on_toggle_doc, on_delete_doc)
        else:
            st.markdown(
                '<div class="doc-meta" style="padding:.4rem .2rem">No documents yet. '
                "Upload a PDF to build your knowledge base.</div>",
                unsafe_allow_html=True,
            )

        st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)
        stats_grid(stats)

        st.markdown('<div class="section-label">Chat history</div>', unsafe_allow_html=True)
        if threads:
            for t in threads:
                st.button(f"🕘  {t['title']}", key=f"th-{t['id']}", use_container_width=True)
        else:
            st.markdown('<div class="doc-meta">No previous chats.</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-label">Settings</div>', unsafe_allow_html=True)
        show_sources = st.toggle("Show sources", value=True)
        show_trace = st.toggle("Show retrieval process", value=True)
        response_style = st.select_slider("Answer style", ["concise", "detailed"], value="detailed")

        if st.button("🧹  Clear chat", use_container_width=True):
            on_clear_chat()

        st.markdown('<div class="section-label">AI pipeline</div>', unsafe_allow_html=True)
        chips = "".join(f'<span class="chip"><span class="tick">✓</span>{p}</span>' for p in PIPELINE)
        st.markdown(f'<div class="pipe">{chips}</div>', unsafe_allow_html=True)

        st.markdown(
            '<hr><div class="doc-meta">Developer</div>'
            '<div style="font-size:12.5px;font-weight:600">Devanshi Vyas</div>',
            unsafe_allow_html=True,
        )

    return {
        "show_sources": show_sources,
        "show_trace": show_trace,
        "response_style": response_style,
    }
