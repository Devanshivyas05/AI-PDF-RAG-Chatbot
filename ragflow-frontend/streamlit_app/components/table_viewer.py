"""Extracted-table viewer with CSV export."""

import io
from typing import Any, Dict

import pandas as pd
import streamlit as st


def table_viewer(table: Dict[str, Any]) -> None:
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:.5rem;margin:.5rem 0 .45rem">
          <span class="badge">▦ Table</span>
          <span class="src-page">{table.get('filename','')} · page {table.get('page','—')}</span>
        </div>
        <div style="font-size:12.8px;font-weight:600;margin-bottom:.35rem">{table.get('title','')}</div>
        """,
        unsafe_allow_html=True,
    )
    df = pd.DataFrame(table.get("rows", []), columns=table.get("columns", []))
    st.dataframe(df, use_container_width=True, hide_index=True)

    buf = io.StringIO()
    df.to_csv(buf, index=False)
    st.download_button(
        "Download CSV",
        buf.getvalue(),
        file_name=f"{table.get('id','table')}.csv",
        mime="text/csv",
        key=f"csv-{table.get('id')}",
    )
