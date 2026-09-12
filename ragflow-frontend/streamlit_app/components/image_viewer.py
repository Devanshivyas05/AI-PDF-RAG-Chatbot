"""Figure / diagram viewer for YOLO-detected images returned by the backend."""

from typing import Any, Dict

import streamlit as st


def image_viewer(figure: Dict[str, Any]) -> None:
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:.5rem;margin:.2rem 0 .45rem">
          <span class="badge">🖼 Figure · {figure.get('detected_by','YOLO')}</span>
          <span class="src-page">{figure.get('filename','')} · page {figure.get('page','—')}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    url = figure.get("url")
    try:
        if url:
            st.image(url, use_container_width=True)
    except Exception:
        st.markdown(
            '<div class="card" style="text-align:center;color:#93A0BA;font-size:12.5px">'
            "Figure preview unavailable — connect the backend image endpoint.</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div style="font-size:12px;color:#93A0BA;margin-top:.35rem">{figure.get("caption","")}</div>',
        unsafe_allow_html=True,
    )
    if figure.get("ocr_text"):
        with st.expander("OCR text"):
            st.code(figure["ocr_text"], language="text")
