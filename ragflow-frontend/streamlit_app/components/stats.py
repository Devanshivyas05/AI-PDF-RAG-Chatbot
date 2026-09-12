"""Knowledge-base overview stats."""

from typing import Dict

import streamlit as st


def _fmt(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}k"
    return str(n)


def stats_grid(stats: Dict[str, int]) -> None:
    items = [
        ("PDFs", stats.get("pdfs", 0)),
        ("Pages", stats.get("pages", 0)),
        ("Chunks", stats.get("chunks", 0)),
        ("Images", stats.get("images", 0)),
        ("Tables", stats.get("tables", 0)),
        ("Indexed", stats.get("pdfs", 0)),
    ]
    cells = "".join(
        f'<div class="stat"><div class="stat-v">{_fmt(v)}</div><div class="stat-k">{k}</div></div>'
        for k, v in items
    )
    st.markdown(f'<div class="stat-grid">{cells}</div>', unsafe_allow_html=True)
