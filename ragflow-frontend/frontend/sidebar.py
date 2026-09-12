# """Sidebar: brand, knowledge base, AI pipeline indicators, developer footer."""

# from typing import Any, Callable, Dict, List

# import streamlit as st

# PIPELINE = [
#     "BGE Embeddings",
#     "ChromaDB",
#     "BM25",
#     "Hybrid Retrieval",
#     "CrossEncoder",
#     "YOLO",
#     "OCR",
#     "Groq LLM",
#     "Conversation Memory",
# ]


# def render_sidebar(
#     pdfs: List[str],
#     selected: List[str],
#     on_toggle: Callable[[str], None],
#     on_upload: Callable[[Any], None],
#     on_new_chat: Callable[[], None],
#     backend_ready: bool,
# ) -> Dict[str, Any]:
#     with st.sidebar:
#         st.markdown(
#             '<div class="sb-brand"><div class="sb-mark"></div>'
#             '<div class="sb-name">RAGFlow</div></div>'
#             '<div class="sb-sub">MULTI-PDF INTELLIGENCE SYSTEM</div>',
#             unsafe_allow_html=True,
#         )
#         st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

#         st.markdown('<div class="sb-head">📚 Knowledge Base</div>', unsafe_allow_html=True)

#         if pdfs:
#             for i, name in enumerate(pdfs):
#                 on = name in selected
#                 cols = st.columns([0.82, 0.18])
#                 with cols[0]:
#                     st.markdown(
#                         f'<div class="doc {"on" if on else ""}">📄'
#                         f'<span class="doc-name">{name}</span></div>',
#                         unsafe_allow_html=True,
#                     )
#                 with cols[1]:
#                     if st.button("✓" if on else "○", key=f"doc-{i}", help="Toggle document"):
#                         on_toggle(name)
#         else:
#             st.markdown(
#                 '<div class="note">No PDFs found in the data folder. Upload one below.</div>',
#                 unsafe_allow_html=True,
#             )

#         uploaded = st.file_uploader(
#             "Upload PDF", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed"
#         )
#         if uploaded:
#             on_upload(uploaded)

#         if st.button("＋  New chat", key="newchat"):
#             on_new_chat()

#         st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
#         st.markdown('<div class="sb-head">⚙️ AI Pipeline</div>', unsafe_allow_html=True)
#         chips = "".join(f'<div class="pchip"><b>✓</b>{p}</div>' for p in PIPELINE)
#         st.markdown(f'<div class="pipe">{chips}</div>', unsafe_allow_html=True)

#         st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
#         st.markdown(
#             '<div class="sb-sub">DEVELOPER</div>'
#             '<div style="font-size:12.5px;font-weight:600">Devanshi Vyas</div>'
#             '<div style="font-size:10.5px;color:#8A97B4">Enterprise Multi-PDF RAG Assistant</div>',
#             unsafe_allow_html=True,
#         )

#     return {"backend_ready": backend_ready}


"""Sidebar: brand, knowledge base, chat history, AI pipeline indicators, developer footer."""

from typing import Any, Callable, Dict, List, Optional

import streamlit as st

PIPELINE = [
    "BGE Embeddings",
    "ChromaDB",
    "BM25",
    "Hybrid Retrieval",
    "CrossEncoder",
    "YOLO",
    "OCR",
    "Groq LLM",
    "Conversation Memory",
]


def render_sidebar(
    pdfs: List[str],
    selected: List[str],
    on_toggle: Callable[[str], None],
    on_upload: Callable[[Any], None],
    on_new_chat: Callable[[], None],
    backend_ready: bool,
    sessions: Optional[List[Dict]] = None,
    current_session_id: Optional[str] = None,
    on_load_session: Optional[Callable[[str], None]] = None,
) -> Dict[str, Any]:
    with st.sidebar:
        st.markdown(
            '<div class="sb-brand"><div class="sb-mark"></div>'
            '<div class="sb-name">RAGFlow</div></div>'
            '<div class="sb-sub">MULTI-PDF INTELLIGENCE SYSTEM</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

        if st.button("＋  New chat", key="newchat", use_container_width=True):
            on_new_chat()

        # -----------------------------------------------------------
        # Chat History (like ChatGPT / Claude's sidebar)
        # -----------------------------------------------------------

        if sessions is not None:

            st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sb-head">💬 Chat History</div>', unsafe_allow_html=True)

            if not sessions:
                st.markdown(
                    '<div class="note">No past chats yet — your questions will '
                    "show up here.</div>",
                    unsafe_allow_html=True,
                )
            else:
                for i, s in enumerate(sessions):

                    is_current = s["session_id"] == current_session_id

                    label = ("🟢 " if is_current else "") + s["title"]

                    if st.button(
                        label,
                        key=f"session-{i}",
                        use_container_width=True,
                        disabled=is_current,
                    ):
                        if on_load_session:
                            on_load_session(s["session_id"])

        st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

        st.markdown('<div class="sb-head">📚 Knowledge Base</div>', unsafe_allow_html=True)

        if pdfs:
            for i, name in enumerate(pdfs):
                on = name in selected
                cols = st.columns([0.82, 0.18])
                with cols[0]:
                    st.markdown(
                        f'<div class="doc {"on" if on else ""}">📄'
                        f'<span class="doc-name">{name}</span></div>',
                        unsafe_allow_html=True,
                    )
                with cols[1]:
                    if st.button("✓" if on else "○", key=f"doc-{i}", help="Toggle document"):
                        on_toggle(name)
        else:
            st.markdown(
                '<div class="note">No PDFs found in the data folder. Upload one below.</div>',
                unsafe_allow_html=True,
            )

        uploaded = st.file_uploader(
            "Upload PDF", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed"
        )
        if uploaded:
            on_upload(uploaded)

        st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-head">⚙️ AI Pipeline</div>', unsafe_allow_html=True)
        chips = "".join(f'<div class="pchip"><b>✓</b>{p}</div>' for p in PIPELINE)
        st.markdown(f'<div class="pipe">{chips}</div>', unsafe_allow_html=True)

        st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sb-sub">DEVELOPER</div>'
            '<div style="font-size:12.5px;font-weight:600">Devanshi Vyas</div>'
            '<div style="font-size:10.5px;color:#8A97B4">Enterprise Multi-PDF RAG Assistant</div>',
            unsafe_allow_html=True,
        )

    return {"backend_ready": backend_ready}