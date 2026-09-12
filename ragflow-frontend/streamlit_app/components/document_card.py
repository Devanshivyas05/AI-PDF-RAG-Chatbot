"""Knowledge-base document row: selection toggle + delete."""

from typing import Any, Callable, Dict

import streamlit as st


def document_card(
    doc: Dict[str, Any],
    selected: bool,
    on_toggle: Callable[[str], None],
    on_delete: Callable[[str], None],
) -> None:
    status = doc.get("status", "ready")
    st.markdown(
        f"""
        <div class="doc {'active' if selected else ''}">
          <span class="dot {status}"></span>
          <div style="min-width:0;flex:1">
            <div class="doc-name">{doc['filename']}</div>
            <div class="doc-meta">{doc.get('pages', 0)} pages · {doc.get('size_label', '—')} · {status}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns([3, 1])
    with c1:
        if st.button(
            "Selected" if selected else "Select",
            key=f"tg-{doc['id']}",
            use_container_width=True,
        ):
            on_toggle(doc["id"])
    with c2:
        if st.button("✕", key=f"del-{doc['id']}", use_container_width=True):
            on_delete(doc["id"])
