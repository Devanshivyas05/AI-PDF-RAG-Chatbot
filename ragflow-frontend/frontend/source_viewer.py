"""Source card, figure/image result, table result and page preview rendering.

All inputs are optional — every renderer degrades gracefully when the backend
omits a field.
"""

import io
import os
from typing import Any, Dict, Optional

import streamlit as st


def _exists(path: Any) -> bool:
    return isinstance(path, str) and bool(path) and os.path.exists(path)


def source_card(pdf: Optional[str], page: Optional[Any], key: str, kind: str = "Text") -> None:
    if not pdf and page is None:
        return
    label = pdf or "Unknown document"
    page_txt = f"Page {page}" if page not in (None, "") else "Page —"
    st.markdown(
        f'<div class="src"><div><div class="src-l">SOURCE</div>'
        f'<div class="src-t">📄 {label}</div></div>'
        f'<span class="badge" style="margin-left:auto">{page_txt}</span>'
        f'<span class="badge">{kind}</span></div>',
        unsafe_allow_html=True,
    )
    with st.expander("View source details"):
        st.markdown(
            f"**Document:** {label}  \n**Page:** {page if page not in (None, '') else '—'}  "
            f"\n**Content type:** {kind}"
        )


def image_result(
    image: Any,
    pdf: Optional[str] = None,
    page: Optional[Any] = None,
    ocr_text: Optional[str] = None,
    key: str = "img",
) -> None:
    """Render a YOLO-detected figure returned by the backend."""
    if not image:
        return
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:.45rem;margin:.6rem 0 .4rem">'
        f'<span class="badge">🖼 Detected Figure</span>'
        f'<span class="src-l">{pdf or ""} {"· Page " + str(page) if page not in (None, "") else ""}</span></div>',
        unsafe_allow_html=True,
    )
    rendered = False
    try:
        if isinstance(image, (bytes, bytearray)):
            st.image(io.BytesIO(image), use_container_width=True)
            rendered = True
        elif _exists(image) or (isinstance(image, str) and image.startswith("http")):
            st.image(image, use_container_width=True)
            rendered = True
        elif not isinstance(image, str):
            st.image(image, use_container_width=True)  # PIL / ndarray
            rendered = True
    except Exception:
        rendered = False

    if not rendered:
        st.markdown(
            '<div class="note">Image not found — the figure referenced by the backend '
            "could not be loaded.</div>",
            unsafe_allow_html=True,
        )
        return

    with st.expander("🔍 View image details"):
        st.markdown(
            f"**Document:** {pdf or '—'}  \n**Page:** {page if page not in (None, '') else '—'}  "
            f"\n**Content type:** Detected figure (YOLO layout detection)"
        )
    if ocr_text:
        with st.expander("OCR Text"):
            st.code(str(ocr_text), language="text")


def table_result(
    table: Any,
    pdf: Optional[str] = None,
    page: Optional[Any] = None,
    key: str = "tbl",
) -> None:
    """Render a table returned by the backend (DataFrame, list, dict or text)."""
    if table is None or (hasattr(table, "empty") and table.empty):
        return
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:.45rem;margin:.7rem 0 .4rem">'
        f'<span class="badge">📊 Relevant Table</span>'
        f'<span class="src-l">{pdf or ""} {"· Page " + str(page) if page not in (None, "") else ""}</span></div>',
        unsafe_allow_html=True,
    )

    df = None
    try:
        import pandas as pd

        if isinstance(table, pd.DataFrame):
            df = table
        elif isinstance(table, dict):
            df = pd.DataFrame(table)
        elif isinstance(table, list):
            df = pd.DataFrame(table)
        elif isinstance(table, str) and _exists(table) and table.lower().endswith(".csv"):
            df = pd.read_csv(table)
    except Exception:
        df = None

    if df is not None:
        st.dataframe(df, use_container_width=True, hide_index=True)
        with st.expander("Expand table"):
            st.dataframe(df, use_container_width=True)
            try:
                st.download_button(
                    "Download CSV",
                    df.to_csv(index=False),
                    file_name=f"{key}.csv",
                    mime="text/csv",
                    key=f"dl-{key}",
                )
            except Exception:
                pass
    elif isinstance(table, str) and table.strip():
        st.markdown(table)
    else:
        st.markdown('<div class="note">Table not found.</div>', unsafe_allow_html=True)

    with st.expander("View source"):
        st.markdown(
            f"**Document:** {pdf or '—'}  \n**Page:** {page if page not in (None, '') else '—'}  "
            f"\n**Content type:** Extracted table"
        )


def page_preview(page_image: Any, pdf: Optional[str] = None, page: Optional[Any] = None) -> None:
    """Small expandable preview of the source page, when available."""
    if not page_image:
        return
    with st.expander(f"📄 Page preview — {pdf or 'document'} · page {page if page not in (None, '') else '—'}"):
        try:
            st.image(page_image, use_container_width=True)
        except Exception:
            st.markdown('<div class="note">Page preview unavailable.</div>', unsafe_allow_html=True)
        st.markdown(
            f"**PDF:** {pdf or '—'}  \n**Page:** {page if page not in (None, '') else '—'}  "
            f"\n**Content type:** Page render"
        )
