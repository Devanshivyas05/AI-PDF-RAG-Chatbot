"""Chat transcript rendering: user bubbles, grounded answers, artefacts, trace."""

from typing import Any, Dict, List

import streamlit as st

from components.image_viewer import image_viewer
from components.source_card import sources_block
from components.table_viewer import table_viewer

PIPELINE_STEPS = [
    "Routing across selected documents…",
    "Semantic search over ChromaDB…",
    "Keyword search with BM25…",
    "Fusing hybrid candidates…",
    "Reranking with CrossEncoder…",
    "Generating grounded answer…",
]


def user_message(content: str) -> None:
    st.markdown(
        f"""
        <div class="msg-row user">
          <div class="bubble-user">{content}</div>
          <div class="avatar">🧑</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def assistant_message(msg: Dict[str, Any], show_sources: bool, show_trace: bool) -> None:
    st.markdown('<div class="msg-row"><div class="avatar ai">✦</div></div>', unsafe_allow_html=True)

    if msg.get("error"):
        st.markdown(f'<div class="err">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="bubble-ai">', unsafe_allow_html=True)
        st.markdown(msg.get("content", ""))
        st.markdown("</div>", unsafe_allow_html=True)

    for fig in msg.get("figures") or []:
        image_viewer(fig)
    for tbl in msg.get("tables") or []:
        table_viewer(tbl)

    if show_sources:
        sources_block(msg.get("sources") or [], msg.get("id", "m"))

    trace: List[Dict[str, str]] = msg.get("trace") or []
    if show_trace and trace:
        with st.expander("View retrieval process"):
            for step in trace:
                st.markdown(
                    f'<div style="display:flex;gap:.5rem;font-size:12px;padding:.15rem 0">'
                    f'<span style="color:#34D399">✓</span><span>{step["label"]}</span>'
                    f'<span style="margin-left:auto;color:#93A0BA">{step.get("detail","")}</span></div>',
                    unsafe_allow_html=True,
                )


def render_transcript(messages: List[Dict[str, Any]], show_sources: bool, show_trace: bool) -> None:
    for msg in messages:
        if msg.get("role") == "user":
            user_message(msg["content"])
        else:
            assistant_message(msg, show_sources, show_trace)
