"""
Enterprise Multi-PDF RAG Chatbot — Streamlit frontend.

Run with:   streamlit run app.py

This file is presentation + state orchestration ONLY.
All backend communication lives in services/api.py.
No RAG logic is implemented here.
"""

from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List

import streamlit as st

from components.chat import PIPELINE_STEPS, assistant_message, render_transcript, user_message
from components.sidebar import render_sidebar
from components.theme import inject_theme
from components.welcome import welcome_screen
from services.api import api

st.set_page_config(
    page_title="Enterprise RAG · Multi-PDF Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_theme()


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
def init_state() -> None:
    ss = st.session_state
    ss.setdefault("messages", [])
    ss.setdefault("documents", api.list_documents())
    ss.setdefault("selected", [d["id"] for d in ss["documents"]])
    ss.setdefault("threads", api.history())
    ss.setdefault("thread_id", str(uuid.uuid4()))
    ss.setdefault("pending", None)
    ss.setdefault("uploaded_names", set())


init_state()


def refresh_documents() -> None:
    st.session_state["documents"] = api.list_documents()


def toggle_doc(doc_id: str) -> None:
    sel = st.session_state["selected"]
    st.session_state["selected"] = [d for d in sel if d != doc_id] if doc_id in sel else sel + [doc_id]


def delete_doc(doc_id: str) -> None:
    api.delete_document(doc_id)
    refresh_documents()
    st.session_state["selected"] = [d for d in st.session_state["selected"] if d != doc_id]
    st.toast("Document removed from knowledge base")


def upload_files(files: List[Any]) -> None:
    added = False
    for f in files:
        if f.name in st.session_state["uploaded_names"]:
            continue
        try:
            doc = api.upload_document(f.name, f.getvalue())
            st.session_state["uploaded_names"].add(f.name)
            st.session_state["selected"].append(doc["id"])
            added = True
        except Exception as exc:  # backend not reachable
            st.toast(f"Upload failed: {exc}")
    if added:
        refresh_documents()
        st.toast("Knowledge base updated")


def new_chat() -> None:
    st.session_state["messages"] = []
    st.session_state["thread_id"] = str(uuid.uuid4())


def clear_chat() -> None:
    st.session_state["messages"] = []


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
settings = render_sidebar(
    documents=st.session_state["documents"],
    selected=st.session_state["selected"],
    stats=api.stats(),
    threads=st.session_state["threads"],
    backend_online=api.health(),
    on_toggle_doc=toggle_doc,
    on_delete_doc=delete_doc,
    on_upload=upload_files,
    on_new_chat=new_chat,
    on_clear_chat=clear_chat,
)


# ---------------------------------------------------------------------------
# Main column
# ---------------------------------------------------------------------------
selected_count = len(st.session_state["selected"])
st.markdown(
    f"""
    <div style="display:flex;align-items:center;justify-content:space-between;gap:1rem;
                border-bottom:1px solid var(--line);padding-bottom:.7rem;margin-bottom:1rem">
      <div>
        <div style="font-family:Sora;font-size:15px;font-weight:600">Document Intelligence Workspace</div>
        <div class="doc-meta">{selected_count} document(s) in scope · hybrid retrieval + reranking</div>
      </div>
      <span class="chip"><span class="tick">✓</span>Grounded answers with citations</span>
    </div>
    """,
    unsafe_allow_html=True,
)

if not st.session_state["messages"] and st.session_state["pending"] is None:
    picked = welcome_screen()
    if picked:
        st.session_state["pending"] = picked
        st.rerun()
else:
    render_transcript(
        st.session_state["messages"],
        settings["show_sources"],
        settings["show_trace"],
    )

prompt = st.chat_input("Ask anything about your documents…")
if prompt:
    st.session_state["pending"] = prompt
    st.rerun()


# ---------------------------------------------------------------------------
# Pending turn -> backend call
# ---------------------------------------------------------------------------
pending = st.session_state["pending"]
if pending:
    st.session_state["messages"].append(
        {"id": str(uuid.uuid4()), "role": "user", "content": pending, "created_at": time.time()}
    )
    user_message(pending)

    placeholder = st.empty()
    with placeholder.container():
        st.markdown('<div class="msg-row"><div class="avatar ai">✦</div></div>', unsafe_allow_html=True)
        status = st.status(PIPELINE_STEPS[0], expanded=True)
        for step in PIPELINE_STEPS[1:]:
            status.write(step)

    try:
        answer: Dict[str, Any] = api.send_message(
            message=pending,
            document_ids=st.session_state["selected"],
            thread_id=st.session_state["thread_id"],
            response_style=settings["response_style"],
        )
    except Exception as exc:
        answer = {
            "id": str(uuid.uuid4()),
            "role": "assistant",
            "content": f"Could not reach the RAG backend. {exc}",
            "created_at": time.time(),
            "error": "backend_unavailable",
        }

    placeholder.empty()
    st.session_state["messages"].append(answer)
    st.session_state["pending"] = None
    st.rerun()
