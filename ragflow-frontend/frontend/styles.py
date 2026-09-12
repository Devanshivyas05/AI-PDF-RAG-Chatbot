import streamlit as st


def inject_styles():
    css = """
    <style>
    /* keep existing CSS exactly as-is */
    /* doc card */
    .doc {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 14px;
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.22);
        background: rgba(15, 23, 42, 0.72);
        color: #e2e8f0;
    }

    /* ... preserve all other existing rules unchanged ... */
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)