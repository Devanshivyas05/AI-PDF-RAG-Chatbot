"""Chat transcript rendering. Display only — conversation memory lives in the backend."""

from typing import Any, Dict, List

import streamlit as st

from frontend.source_viewer import image_result, page_preview, source_card, table_result

NO_INFO = "No relevant information was found in the selected documents."


def render_user(content: str) -> None:
    with st.chat_message("user", avatar="🧑"):
        st.markdown(content)


def render_assistant(payload: Dict[str, Any], key: str = "m") -> None:
    with st.chat_message("assistant", avatar="🧠"):
        if payload.get("error"):
            st.markdown(f'<div class="err">{payload["error"]}</div>', unsafe_allow_html=True)
            return

        answer = payload.get("answer")
        has_extra = any(payload.get(k) for k in ("image", "table", "page_image"))
        if answer:
            st.markdown(answer)
        elif not has_extra:
            st.markdown(f'<div class="note">{NO_INFO}</div>', unsafe_allow_html=True)

        pdf = payload.get("pdf")
        page = payload.get("page")

        if payload.get("image"):
            image_result(payload["image"], pdf, page, payload.get("ocr_text"), key=f"{key}-img")
        if payload.get("table") is not None:
            table_result(payload["table"], pdf, page, key=f"{key}-tbl")
        if payload.get("page_image"):
            page_preview(payload["page_image"], pdf, page)

        if pdf or page not in (None, ""):
            kind = "Figure" if payload.get("image") else ("Table" if payload.get("table") is not None else "Text")
            source_card(pdf, page, key=f"{key}-src", kind=kind)


def render_transcript(messages: List[Dict[str, Any]]) -> None:
    for i, msg in enumerate(messages):
        if msg.get("role") == "user":
            render_user(msg.get("content", ""))
        else:
            render_assistant(msg.get("payload", {}), key=f"m{i}")
