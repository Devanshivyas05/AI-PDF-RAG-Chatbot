"""Empty-state hero: capability framing + example prompts."""

from typing import Optional

import streamlit as st

EXAMPLES = [
    ("📘", "Explain the main concepts in this PDF"),
    ("🖼", "Show me the CNN architecture diagram"),
    ("▦", "Find the optimizer comparison table"),
    ("🔎", "Summarize this chapter"),
    ("∑", "What are the important formulas?"),
    ("⚖", "List the key compliance risks"),
]

FLOW = ["Documents", "Hybrid retrieval", "Reranking", "AI answer", "Sources · Images · Tables"]


def welcome_screen() -> Optional[str]:
    st.markdown(
        """
        <div class="hero">
          <div class="hero-mark">✦</div>
          <h1>Ask your documents anything.</h1>
          <p>Enterprise multi-PDF retrieval with grounded answers, figures and tables.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    picked: Optional[str] = None
    cols = st.columns(3)
    for i, (icon, text) in enumerate(EXAMPLES):
        with cols[i % 3]:
            if st.button(f"{icon}  {text}", key=f"ex-{i}", use_container_width=True):
                picked = text

    steps = f'<span class="arrow">→</span>'.join(f'<span class="step">{s}</span>' for s in FLOW)
    st.markdown(
        f'<div class="flow" style="margin-top:1.6rem">{steps}</div>',
        unsafe_allow_html=True,
    )
    return picked
