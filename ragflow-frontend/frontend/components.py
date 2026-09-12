"""Reusable presentation blocks: header, hero, stats, status, examples, errors."""

from typing import Any, Dict, List, Optional

import streamlit as st

PIPELINE_STATUS_STEPS = [
    "PDF routing",
    "Semantic retrieval",
    "BM25 retrieval",
    "CrossEncoder reranking",
]

EXAMPLES = [
    "Explain the main concepts in this document",
    "Show me the CNN architecture diagram",
    "Find the table about classification algorithms",
    "Summarize this document",
    "Explain this diagram",
]


def header() -> None:
    st.markdown(
        """
        <div class="hdr">
          <div class="hdr-mark">🧠</div>
          <div>
            <div class="hdr-title">RAGFlow</div>
            <div class="hdr-sub">Enterprise Multi-PDF Intelligence Assistant ·
              Ask questions across your documents using hybrid retrieval and grounded AI.</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero() -> None:
    st.markdown(
        """
        <div class="hero">
          <span class="pill">● AI KNOWLEDGE ENGINE</span>
          <h2>Ask your documents anything.</h2>
          <p>Search across your PDF knowledge base using hybrid retrieval, semantic embeddings,
          BM25 ranking and CrossEncoder reranking — then generate grounded answers using Groq LLM.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stats_row(stats: Dict[str, Any]) -> None:
    items = [
        ("📄", "Documents", str(stats.get("documents", 0))),
        ("🔎", "Retrieval", str(stats.get("retrieval", "Hybrid"))),
        ("🧠", "Embeddings", str(stats.get("embeddings", "BGE"))),
        ("⚡", "LLM", str(stats.get("llm", "Groq"))),
    ]
    cols = st.columns(4)
    for col, (icon, key, val) in zip(cols, items):
        with col:
            st.markdown(
                f'<div class="stat"><div class="stat-k">{icon} {key}</div>'
                f'<div class="stat-v">{val}</div></div>',
                unsafe_allow_html=True,
            )


def example_questions() -> Optional[str]:
    """Compact example cards; returns the clicked question."""
    st.markdown('<div class="sb-sub">TRY AN EXAMPLE</div>', unsafe_allow_html=True)
    picked: Optional[str] = None
    cols = st.columns(3)
    for i, q in enumerate(EXAMPLES):
        with cols[i % 3]:
            if st.button(q, key=f"ex-{i}", use_container_width=True):
                picked = q
    return picked


def status_panel(container, done: List[str], current: str) -> None:
    """Render the processing status (visual only — no fake backend claims)."""
    lines = "".join(f'<div class="step"><b>✓</b> {s}</div>' for s in done)
    lines += f'<div class="step">⏳ {current}</div>'
    container.markdown(
        f'<div class="note"><div style="font-weight:600;color:#E9EDF7;margin-bottom:.3rem">'
        f"🔄 Processing your question…</div>{lines}</div>",
        unsafe_allow_html=True,
    )


def error_box(message: str) -> None:
    st.markdown(f'<div class="err">{message}</div>', unsafe_allow_html=True)


def note_box(message: str) -> None:
    st.markdown(f'<div class="note">{message}</div>', unsafe_allow_html=True)
