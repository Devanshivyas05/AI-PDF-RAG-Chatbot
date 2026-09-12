# # """
# # RAGFlow — Enterprise Multi-PDF Intelligence Assistant (Streamlit frontend).

# # Run with:   streamlit run frontend.py

# # This file is layout + session state ONLY.
# # All RAG work is done by the EXISTING backend in src/rag_pipeline.py,
# # reached through services/rag_service.py. No RAG logic lives here.
# # """

# # from __future__ import annotations

# # import os
# # import time
# # from typing import Any, Dict, List

# # import streamlit as st

# # from frontend.chat import render_assistant, render_transcript, render_user
# # from frontend.components import (
# #     PIPELINE_STATUS_STEPS,
# #     error_box,
# #     example_questions,
# #     header,
# #     hero,
# #     note_box,
# #     stats_row,
# #     status_panel,
# # )
# # from frontend.sidebar import render_sidebar
# # from frontend.styles import inject_styles
# # from services.rag_service import get_service

# # DATA_FOLDER = os.environ.get("RAG_DATA_FOLDER", "data")

# # st.set_page_config(
# #     page_title="RAGFlow · Enterprise Multi-PDF Intelligence Assistant",
# #     page_icon="🧠",
# #     layout="wide",
# #     initial_sidebar_state="expanded",
# # )
# # inject_styles()


# # # ---------------------------------------------------------------------------
# # # Backend (built once per process)
# # # ---------------------------------------------------------------------------
# # @st.cache_resource(show_spinner=False)
# # def boot_service(data_folder: str):
# #     svc = get_service(data_folder)
# #     svc.initialize(data_folder)
# #     return svc


# # with st.spinner("Initializing RAG knowledge engine…"):
# #     service = boot_service(DATA_FOLDER)


# # # ---------------------------------------------------------------------------
# # # UI state
# # # ---------------------------------------------------------------------------
# # ss = st.session_state
# # ss.setdefault("messages", [])
# # ss.setdefault("pending", None)
# # pdfs: List[str] = service.list_pdfs()
# # ss.setdefault("selected", list(pdfs))


# # def toggle_doc(name: str) -> None:
# #     sel = ss["selected"]
# #     ss["selected"] = [d for d in sel if d != name] if name in sel else sel + [name]


# # def upload_pdfs(files: List[Any]) -> None:
# #     for f in files:
# #         try:
# #             service.save_uploaded_pdf(f.name, f.getvalue())
# #             if f.name not in ss["selected"]:
# #                 ss["selected"].append(f.name)
# #         except Exception as exc:
# #             st.toast(f"Could not add {f.name}: {exc}")
# #     st.toast("Knowledge base updated")


# # def new_chat() -> None:
# #     ss["messages"] = []
# #     ss["pending"] = None


# # render_sidebar(
# #     pdfs=pdfs,
# #     selected=ss["selected"],
# #     on_toggle=toggle_doc,
# #     on_upload=upload_pdfs,
# #     on_new_chat=new_chat,
# #     backend_ready=service.ready,
# # )


# # # ---------------------------------------------------------------------------
# # # Main
# # # ---------------------------------------------------------------------------
# # header()

# # if not ss["messages"] and ss["pending"] is None:
# #     hero()
# #     stats_row(service.stats())

# #     if not pdfs:
# #         note_box("No PDFs found in the data folder. Add documents to start querying.")
# #     if not service.ready:
# #         error_box(service.error or "Backend not initialized.")

# #     picked = example_questions()
# #     if picked:
# #         ss["pending"] = picked
# #         st.rerun()
# # else:
# #     render_transcript(ss["messages"])

# # prompt = st.chat_input("Ask anything about your PDFs...")
# # if prompt:
# #     ss["pending"] = prompt
# #     st.rerun()


# # # ---------------------------------------------------------------------------
# # # Pending turn -> existing backend
# # # ---------------------------------------------------------------------------
# # pending = ss["pending"]
# # if pending:
# #     ss["messages"].append({"role": "user", "content": pending})
# #     render_user(pending)

# #     slot = st.empty()
# #     status_panel(slot, [], "Sending request to the RAG pipeline…")

# #     payload: Dict[str, Any] = service.ask(pending)

# #     slot.empty()
# #     ss["messages"].append({"role": "assistant", "payload": payload})
# #     ss["pending"] = None
# #     st.rerun()


# """
# RAGFlow — Enterprise Multi-PDF Intelligence Assistant (Streamlit frontend).

# Run with:   streamlit run frontend.py

# This file is layout + session state ONLY.
# All RAG work is done by the EXISTING backend in src/rag_pipeline.py,
# reached through services/rag_service.py. No RAG logic lives here.
# """

# from __future__ import annotations

# import os
# import time
# from typing import Any, Dict, List

# import streamlit as st

# from database import crud
# from frontend.chat import render_assistant, render_transcript, render_user
# from frontend.components import (
#     PIPELINE_STATUS_STEPS,
#     error_box,
#     example_questions,
#     header,
#     hero,
#     note_box,
#     stats_row,
#     status_panel,
# )
# from frontend.sidebar import render_sidebar
# from frontend.styles import inject_styles
# from services.rag_service import get_service

# DATA_FOLDER = os.environ.get("RAG_DATA_FOLDER", "data")

# # No login system exists yet, so every chat is logged under a fixed
# # user id. Point this at a real users.id row (see your `users` table)
# # or set RAGFLOW_USER_ID in .env once authentication is added.
# DEFAULT_USER_ID = int(os.environ.get("RAGFLOW_USER_ID", "1"))

# st.set_page_config(
#     page_title="RAGFlow · Enterprise Multi-PDF Intelligence Assistant",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )
# inject_styles()


# # ---------------------------------------------------------------------------
# # Backend (built once per process)
# # ---------------------------------------------------------------------------
# @st.cache_resource(show_spinner=False)
# def boot_service(data_folder: str):
#     svc = get_service(data_folder)
#     svc.initialize(data_folder)
#     return svc


# with st.spinner("Initializing RAG knowledge engine…"):
#     service = boot_service(DATA_FOLDER)


# # ---------------------------------------------------------------------------
# # UI state
# # ---------------------------------------------------------------------------
# ss = st.session_state
# ss.setdefault("messages", [])
# ss.setdefault("pending", None)
# pdfs: List[str] = service.list_pdfs()
# ss.setdefault("selected", list(pdfs))


# def toggle_doc(name: str) -> None:
#     sel = ss["selected"]
#     ss["selected"] = [d for d in sel if d != name] if name in sel else sel + [name]


# def upload_pdfs(files: List[Any]) -> None:
#     for f in files:
#         try:
#             service.save_uploaded_pdf(f.name, f.getvalue())
#             if f.name not in ss["selected"]:
#                 ss["selected"].append(f.name)
#         except Exception as exc:
#             st.toast(f"Could not add {f.name}: {exc}")
#     st.toast("Knowledge base updated")


# def new_chat() -> None:
#     # Purely a UI reset — the current schema has no conversations table
#     # to group messages under, so each Q&A is logged independently in
#     # conversation_history regardless of which chat "session" it's in.
#     ss["messages"] = []
#     ss["pending"] = None


# render_sidebar(
#     pdfs=pdfs,
#     selected=ss["selected"],
#     on_toggle=toggle_doc,
#     on_upload=upload_pdfs,
#     on_new_chat=new_chat,
#     backend_ready=service.ready,
# )


# # ---------------------------------------------------------------------------
# # Main
# # ---------------------------------------------------------------------------
# header()

# if not ss["messages"] and ss["pending"] is None:
#     hero()
#     stats_row(service.stats())

#     if not pdfs:
#         note_box("No PDFs found in the data folder. Add documents to start querying.")
#     if not service.ready:
#         error_box(service.error or "Backend not initialized.")

#     picked = example_questions()
#     if picked:
#         ss["pending"] = picked
#         st.rerun()
# else:
#     render_transcript(ss["messages"])

# prompt = st.chat_input("Ask anything about your PDFs...")
# if prompt:
#     ss["pending"] = prompt
#     st.rerun()


# # ---------------------------------------------------------------------------
# # Pending turn -> existing backend
# # ---------------------------------------------------------------------------
# pending = ss["pending"]
# if pending:
#     ss["messages"].append({"role": "user", "content": pending})
#     render_user(pending)

#     slot = st.empty()
#     status_panel(slot, [], "Sending request to the RAG pipeline…")

#     start_time = time.time()
#     payload: Dict[str, Any] = service.ask(pending)
#     latency_ms = (time.time() - start_time) * 1000

#     slot.empty()
#     ss["messages"].append({"role": "assistant", "payload": payload})
#     ss["pending"] = None

#     # -----------------------------------------------------------------
#     # Persist this turn to MySQL. Logging failures are swallowed inside
#     # crud.py so a DB hiccup never breaks the chat the user is having.
#     # -----------------------------------------------------------------
#     has_error = bool(payload.get("error"))

#     crud.log_conversation(
#         user_id=DEFAULT_USER_ID,
#         question=pending,
#         answer=payload.get("answer"),
#         document_name=", ".join(ss["selected"]) if ss["selected"] else None,
#     )

#     crud.log_query_metric(
#         user_id=DEFAULT_USER_ID,
#         latency_ms=latency_ms,
#         query_type="chat",
#         status="error" if has_error else "success",
#     )

#     st.rerun()


"""
RAGFlow — Enterprise Multi-PDF Intelligence Assistant (Streamlit frontend).

Run with:   streamlit run frontend.py

This file is layout + session state ONLY.
All RAG work is done by the EXISTING backend in src/rag_pipeline.py,
reached through services/rag_service.py. No RAG logic lives here.
"""

from __future__ import annotations

import os
import time
import uuid
from typing import Any, Dict, List

import streamlit as st

from database import crud
from frontend.chat import render_assistant, render_transcript, render_user
from frontend.components import (
    PIPELINE_STATUS_STEPS,
    error_box,
    example_questions,
    header,
    hero,
    note_box,
    stats_row,
    status_panel,
)
from frontend.sidebar import render_sidebar
from frontend.styles import inject_styles
from services.rag_service import get_service

DATA_FOLDER = os.environ.get("RAG_DATA_FOLDER", "data")

# No login system exists yet, so every chat is logged under a fixed
# user id. Point this at a real users.id row (see your `users` table)
# or set RAGFLOW_USER_ID in .env once authentication is added.
DEFAULT_USER_ID = int(os.environ.get("RAGFLOW_USER_ID", "1"))

st.set_page_config(
    page_title="RAGFlow · Enterprise Multi-PDF Intelligence Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_styles()


# ---------------------------------------------------------------------------
# Backend (built once per process)
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def boot_service(data_folder: str):
    svc = get_service(data_folder)
    svc.initialize(data_folder)
    return svc


with st.spinner("Initializing RAG knowledge engine…"):
    service = boot_service(DATA_FOLDER)


# ---------------------------------------------------------------------------
# UI state
# ---------------------------------------------------------------------------
ss = st.session_state
ss.setdefault("messages", [])
ss.setdefault("pending", None)
ss.setdefault("session_id", str(uuid.uuid4()))
pdfs: List[str] = service.list_pdfs()
ss.setdefault("selected", list(pdfs))


def toggle_doc(name: str) -> None:
    sel = ss["selected"]
    ss["selected"] = [d for d in sel if d != name] if name in sel else sel + [name]


def upload_pdfs(files: List[Any]) -> None:
    for f in files:
        try:
            service.save_uploaded_pdf(f.name, f.getvalue())
            if f.name not in ss["selected"]:
                ss["selected"].append(f.name)
        except Exception as exc:
            st.toast(f"Could not add {f.name}: {exc}")
    st.toast("Knowledge base updated")


def new_chat() -> None:
    # Start a brand new session id so this chat's Q&A turns are grouped
    # separately from any previous chat in the sidebar history.
    ss["messages"] = []
    ss["pending"] = None
    ss["session_id"] = str(uuid.uuid4())


def load_session(session_id: str) -> None:
    """Switch to a past chat from the sidebar, rebuilding the transcript."""

    rows = crud.get_session_messages(DEFAULT_USER_ID, session_id)

    messages: List[Dict[str, Any]] = []

    for row in rows:
        messages.append({"role": "user", "content": row["question"]})
        messages.append({"role": "assistant", "payload": {"answer": row["answer"]}})

    ss["messages"] = messages
    ss["pending"] = None
    ss["session_id"] = session_id


# Sidebar history list — fetched fresh each render so a brand new chat
# shows up as soon as it has its first message.
recent_sessions = crud.get_recent_sessions(DEFAULT_USER_ID)

render_sidebar(
    pdfs=pdfs,
    selected=ss["selected"],
    on_toggle=toggle_doc,
    on_upload=upload_pdfs,
    on_new_chat=new_chat,
    backend_ready=service.ready,
    sessions=recent_sessions,
    current_session_id=ss["session_id"],
    on_load_session=load_session,
)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
header()

if not ss["messages"] and ss["pending"] is None:
    hero()
    stats_row(service.stats())

    if not pdfs:
        note_box("No PDFs found in the data folder. Add documents to start querying.")
    if not service.ready:
        error_box(service.error or "Backend not initialized.")

    picked = example_questions()
    if picked:
        ss["pending"] = picked
        st.rerun()
else:
    render_transcript(ss["messages"])

prompt = st.chat_input("Ask anything about your PDFs...")
if prompt:
    ss["pending"] = prompt
    st.rerun()


# ---------------------------------------------------------------------------
# Pending turn -> existing backend
# ---------------------------------------------------------------------------
pending = ss["pending"]
if pending:
    ss["messages"].append({"role": "user", "content": pending})
    render_user(pending)

    slot = st.empty()
    status_panel(slot, [], "Sending request to the RAG pipeline…")

    start_time = time.time()
    payload: Dict[str, Any] = service.ask(pending)
    latency_ms = (time.time() - start_time) * 1000

    slot.empty()
    ss["messages"].append({"role": "assistant", "payload": payload})
    ss["pending"] = None

    # -----------------------------------------------------------------
    # Persist this turn to MySQL. Logging failures are swallowed inside
    # crud.py so a DB hiccup never breaks the chat the user is having.
    # -----------------------------------------------------------------
    has_error = bool(payload.get("error"))

    crud.log_conversation(
        user_id=DEFAULT_USER_ID,
        session_id=ss["session_id"],
        question=pending,
        answer=payload.get("answer"),
        document_name=", ".join(ss["selected"]) if ss["selected"] else None,
    )

    crud.log_query_metric(
        user_id=DEFAULT_USER_ID,
        latency_ms=latency_ms,
        query_type="chat",
        status="error" if has_error else "success",
    )

    st.rerun()