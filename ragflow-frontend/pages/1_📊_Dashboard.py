"""
Usage Dashboard — queries per day, latency trends, document and user
activity, all pulled from conversation_history / query_metrics.

Streamlit auto-discovers files in a `pages/` folder next to the main
entrypoint and lists them as separate nav items, so this file needs no
wiring into frontend.py at all.
"""

import streamlit as st

from database import crud

st.set_page_config(
    page_title="RAGFlow · Usage Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Usage Dashboard")

days = st.selectbox(
    "Time range",
    options=[7, 14, 30, 90],
    index=2,
    format_func=lambda d: f"Last {d} days",
)

# ---------------------------------------------------------------------
# Headline numbers
# ---------------------------------------------------------------------

stats = crud.get_summary_stats(days=days)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Queries", stats["total_queries"])
col2.metric("Active Users", stats["active_users"])
col3.metric("Documents Used", stats["documents_used"])
col4.metric("Avg Latency", f"{stats['avg_latency_ms']:.0f} ms" if stats["avg_latency_ms"] else "—")
col5.metric("Success Rate", f"{stats['success_rate']:.1f}%" if stats["success_rate"] else "—")

st.divider()

# ---------------------------------------------------------------------
# Queries per day
# ---------------------------------------------------------------------

st.subheader("Queries per day")

queries_df = crud.get_queries_per_day(days=days)

if queries_df.empty:
    st.info("No query data yet for this time range.")
else:
    st.line_chart(
        queries_df.set_index("query_date")["total_queries"],
        use_container_width=True,
    )

# ---------------------------------------------------------------------
# Latency over time
# ---------------------------------------------------------------------

st.subheader("Latency over time")

latency_df = crud.get_latency_over_time(days=days)

if latency_df.empty:
    st.info("No latency data yet for this time range.")
else:
    st.line_chart(
        latency_df.set_index("query_date")["avg_latency_ms"],
        use_container_width=True,
    )

col_left, col_right = st.columns(2)

# ---------------------------------------------------------------------
# Document usage
# ---------------------------------------------------------------------

with col_left:

    st.subheader("Most queried documents")

    doc_df = crud.get_document_usage(days=days)

    if doc_df.empty:
        st.info("No document usage data yet.")
    else:
        st.bar_chart(
            doc_df.set_index("document_name")["total_queries"],
            use_container_width=True,
        )

# ---------------------------------------------------------------------
# User usage
# ---------------------------------------------------------------------

with col_right:

    st.subheader("User activity")

    user_df = crud.get_user_usage(days=days)

    if user_df.empty:
        st.info("No user activity data yet.")
    else:
        st.dataframe(
            user_df.rename(columns={
                "name": "User",
                "total_queries": "Queries",
                "avg_latency_ms": "Avg Latency (ms)",
            })[["User", "Queries", "Avg Latency (ms)"]],
            use_container_width=True,
            hide_index=True,
        )