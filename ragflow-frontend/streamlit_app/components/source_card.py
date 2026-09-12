"""Citation card + retrieval score breakdown panel."""

from typing import Any, Dict, List

import streamlit as st


def _score_bar(label: str, value: float) -> str:
    pct = max(0, min(100, value * 100))
    return (
        f'<div style="margin-bottom:.55rem">'
        f'<div class="sb-top"><span>{label}</span><b>{value:.3f}</b></div>'
        f'<div class="sb"><i style="width:{pct:.1f}%"></i></div></div>'
    )


def source_card(source: Dict[str, Any], key: str) -> None:
    st.markdown(
        f"""
        <div class="src">
          <div style="display:flex;align-items:center;gap:.5rem">
            <span>📄</span>
            <div style="min-width:0;flex:1">
              <div class="src-title">{source['filename']}</div>
              <div class="src-page">Page {source['page']}</div>
            </div>
            <span class="badge">{round(source.get('relevance', 0) * 100)}%</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Inspect retrieval", expanded=False):
        st.markdown(
            f'<div style="font-size:12.5px;line-height:1.7;color:#C7D0E4">{source["chunk"]}</div>',
            unsafe_allow_html=True,
        )
        s = source.get("scores", {})
        st.markdown(
            "<div style='margin-top:.8rem'>"
            + _score_bar("Semantic (ChromaDB)", float(s.get("semantic", 0)))
            + _score_bar("Keyword (BM25)", float(s.get("bm25", 0)))
            + _score_bar("Rerank (CrossEncoder)", float(s.get("rerank", 0)))
            + "</div>",
            unsafe_allow_html=True,
        )


def sources_block(sources: List[Dict[str, Any]], msg_id: str) -> None:
    if not sources:
        return
    st.markdown('<div class="section-label">Sources</div>', unsafe_allow_html=True)
    cols = st.columns(min(2, len(sources)))
    for i, src in enumerate(sources):
        with cols[i % len(cols)]:
            source_card(src, key=f"{msg_id}-{i}")
