# # """
# # Database write helpers for RAGFlow.

# # Matches the ACTUAL live schema in ragflow_db:

# # conversation_history(id, user_id, answer, question, timestamp, document_name)
# # query_metrics(id, user_id, timestamp, latency_ms, query_type, status)

# # Both functions swallow and log DB errors rather than raising, so a
# # database hiccup never breaks the chat UI — the user still gets their
# # answer even if logging fails.
# # """

# # from typing import Optional

# # from sqlalchemy import text

# # from database.connection import SessionLocal


# # def log_conversation(
# #     user_id: int,
# #     question: str,
# #     answer: Optional[str],
# #     document_name: Optional[str] = None,
# # ) -> None:
# #     """Insert one Q&A turn into conversation_history."""

# #     session = SessionLocal()

# #     try:
# #         session.execute(
# #             text(
# #                 """
# #                 INSERT INTO conversation_history
# #                     (user_id, question, answer, document_name)
# #                 VALUES
# #                     (:user_id, :question, :answer, :document_name)
# #                 """
# #             ),
# #             {
# #                 "user_id": user_id,
# #                 "question": question,
# #                 "answer": answer,
# #                 "document_name": document_name,
# #             },
# #         )
# #         session.commit()

# #     except Exception as exc:

# #         session.rollback()
# #         print(f"[DB] Failed to log conversation: {exc}", flush=True)

# #     finally:
# #         session.close()


# # def log_query_metric(
# #     user_id: int,
# #     latency_ms: float,
# #     query_type: str = "chat",
# #     status: str = "success",
# # ) -> None:
# #     """Insert one performance record into query_metrics."""

# #     session = SessionLocal()

# #     try:
# #         session.execute(
# #             text(
# #                 """
# #                 INSERT INTO query_metrics
# #                     (user_id, latency_ms, query_type, status)
# #                 VALUES
# #                     (:user_id, :latency_ms, :query_type, :status)
# #                 """
# #             ),
# #             {
# #                 "user_id": user_id,
# #                 "latency_ms": latency_ms,
# #                 "query_type": query_type,
# #                 "status": status,
# #             },
# #         )
# #         session.commit()

# #     except Exception as exc:

# #         session.rollback()
# #         print(f"[DB] Failed to log query metric: {exc}", flush=True)

# #     finally:
# #         session.close()

# """
# Database write/read helpers for RAGFlow.

# Matches the ACTUAL live schema in ragflow_db, PLUS one added column:

# conversation_history(
#     id, user_id, session_id, answer, question, timestamp, document_name
# )
# query_metrics(id, user_id, timestamp, latency_ms, query_type, status)

# session_id groups multiple Q&A turns into one chat "session," the same
# way ChatGPT/Claude group messages into a conversation thread. It is
# generated client-side (frontend.py) as a UUID string — no separate
# "create session" DB call is needed.

# All functions swallow and log DB errors rather than raising, so a
# database hiccup never breaks the chat UI.
# """

# from typing import Dict, List, Optional

# from sqlalchemy import text

# from database.connection import SessionLocal


# def log_conversation(
#     user_id: int,
#     session_id: str,
#     question: str,
#     answer: Optional[str],
#     document_name: Optional[str] = None,
# ) -> None:
#     """Insert one Q&A turn into conversation_history, tagged to a session."""

#     session = SessionLocal()

#     try:
#         session.execute(
#             text(
#                 """
#                 INSERT INTO conversation_history
#                     (user_id, session_id, question, answer, document_name)
#                 VALUES
#                     (:user_id, :session_id, :question, :answer, :document_name)
#                 """
#             ),
#             {
#                 "user_id": user_id,
#                 "session_id": session_id,
#                 "question": question,
#                 "answer": answer,
#                 "document_name": document_name,
#             },
#         )
#         session.commit()

#     except Exception as exc:

#         session.rollback()
#         print(f"[DB] Failed to log conversation: {exc}", flush=True)

#     finally:
#         session.close()


# def log_query_metric(
#     user_id: int,
#     latency_ms: float,
#     query_type: str = "chat",
#     status: str = "success",
# ) -> None:
#     """Insert one performance record into query_metrics."""

#     session = SessionLocal()

#     try:
#         session.execute(
#             text(
#                 """
#                 INSERT INTO query_metrics
#                     (user_id, latency_ms, query_type, status)
#                 VALUES
#                     (:user_id, :latency_ms, :query_type, :status)
#                 """
#             ),
#             {
#                 "user_id": user_id,
#                 "latency_ms": latency_ms,
#                 "query_type": query_type,
#                 "status": status,
#             },
#         )
#         session.commit()

#     except Exception as exc:

#         session.rollback()
#         print(f"[DB] Failed to log query metric: {exc}", flush=True)

#     finally:
#         session.close()


# def get_recent_sessions(user_id: int, limit: int = 20) -> List[Dict]:
#     """
#     Return recent chat sessions for the sidebar, newest first.

#     Each entry: {"session_id": ..., "title": <first question, truncated>,
#     "last_timestamp": ...}. Rows with no session_id (old data from before
#     this feature existed) are excluded.
#     """

#     session = SessionLocal()

#     try:
#         result = session.execute(
#             text(
#                 """
#                 SELECT
#                     session_id,
#                     MIN(question)  AS first_question,
#                     MAX(timestamp) AS last_timestamp
#                 FROM conversation_history
#                 WHERE user_id = :user_id
#                   AND session_id IS NOT NULL
#                 GROUP BY session_id
#                 ORDER BY last_timestamp DESC
#                 LIMIT :limit
#                 """
#             ),
#             {"user_id": user_id, "limit": limit},
#         )

#         rows = result.mappings().all()

#         sessions = []

#         for row in rows:

#             title = (row["first_question"] or "Untitled chat").strip()

#             if len(title) > 40:
#                 title = title[:40].rstrip() + "…"

#             sessions.append({
#                 "session_id": row["session_id"],
#                 "title": title,
#                 "last_timestamp": row["last_timestamp"],
#             })

#         return sessions

#     except Exception as exc:

#         print(f"[DB] Failed to load recent sessions: {exc}", flush=True)
#         return []

#     finally:
#         session.close()


# def get_session_messages(user_id: int, session_id: str) -> List[Dict]:
#     """
#     Return every Q&A turn for one session, oldest first, so the
#     frontend can rebuild ss['messages'] exactly as it looked live.
#     """

#     session = SessionLocal()

#     try:
#         result = session.execute(
#             text(
#                 """
#                 SELECT question, answer, timestamp
#                 FROM conversation_history
#                 WHERE user_id = :user_id
#                   AND session_id = :session_id
#                 ORDER BY timestamp ASC, id ASC
#                 """
#             ),
#             {"user_id": user_id, "session_id": session_id},
#         )

#         return [dict(row) for row in result.mappings().all()]

#     except Exception as exc:

#         print(f"[DB] Failed to load session messages: {exc}", flush=True)
#         return []

#     finally:
#         session.close()


"""
Database write/read helpers for RAGFlow.

Matches the ACTUAL live schema in ragflow_db, PLUS one added column:

conversation_history(
    id, user_id, session_id, answer, question, timestamp, document_name
)
query_metrics(id, user_id, timestamp, latency_ms, query_type, status)

session_id groups multiple Q&A turns into one chat "session," the same
way ChatGPT/Claude group messages into a conversation thread. It is
generated client-side (frontend.py) as a UUID string — no separate
"create session" DB call is needed.

All functions swallow and log DB errors rather than raising, so a
database hiccup never breaks the chat UI.
"""

from typing import Dict, List, Optional

import pandas as pd
from sqlalchemy import text

from database.connection import SessionLocal


def log_conversation(
    user_id: int,
    session_id: str,
    question: str,
    answer: Optional[str],
    document_name: Optional[str] = None,
) -> None:
    """Insert one Q&A turn into conversation_history, tagged to a session."""

    session = SessionLocal()

    try:
        session.execute(
            text(
                """
                INSERT INTO conversation_history
                    (user_id, session_id, question, answer, document_name)
                VALUES
                    (:user_id, :session_id, :question, :answer, :document_name)
                """
            ),
            {
                "user_id": user_id,
                "session_id": session_id,
                "question": question,
                "answer": answer,
                "document_name": document_name,
            },
        )
        session.commit()

    except Exception as exc:

        session.rollback()
        print(f"[DB] Failed to log conversation: {exc}", flush=True)

    finally:
        session.close()


def log_query_metric(
    user_id: int,
    latency_ms: float,
    query_type: str = "chat",
    status: str = "success",
) -> None:
    """Insert one performance record into query_metrics."""

    session = SessionLocal()

    try:
        session.execute(
            text(
                """
                INSERT INTO query_metrics
                    (user_id, latency_ms, query_type, status)
                VALUES
                    (:user_id, :latency_ms, :query_type, :status)
                """
            ),
            {
                "user_id": user_id,
                "latency_ms": latency_ms,
                "query_type": query_type,
                "status": status,
            },
        )
        session.commit()

    except Exception as exc:

        session.rollback()
        print(f"[DB] Failed to log query metric: {exc}", flush=True)

    finally:
        session.close()


def get_recent_sessions(user_id: int, limit: int = 20) -> List[Dict]:
    """
    Return recent chat sessions for the sidebar, newest first.

    Each entry: {"session_id": ..., "title": <first question, truncated>,
    "last_timestamp": ...}. Rows with no session_id (old data from before
    this feature existed) are excluded.
    """

    session = SessionLocal()

    try:
        result = session.execute(
            text(
                """
                SELECT
                    session_id,
                    MIN(question)  AS first_question,
                    MAX(timestamp) AS last_timestamp
                FROM conversation_history
                WHERE user_id = :user_id
                  AND session_id IS NOT NULL
                GROUP BY session_id
                ORDER BY last_timestamp DESC
                LIMIT :limit
                """
            ),
            {"user_id": user_id, "limit": limit},
        )

        rows = result.mappings().all()

        sessions = []

        for row in rows:

            title = (row["first_question"] or "Untitled chat").strip()

            if len(title) > 40:
                title = title[:40].rstrip() + "…"

            sessions.append({
                "session_id": row["session_id"],
                "title": title,
                "last_timestamp": row["last_timestamp"],
            })

        return sessions

    except Exception as exc:

        print(f"[DB] Failed to load recent sessions: {exc}", flush=True)
        return []

    finally:
        session.close()


def get_session_messages(user_id: int, session_id: str) -> List[Dict]:
    """
    Return every Q&A turn for one session, oldest first, so the
    frontend can rebuild ss['messages'] exactly as it looked live.
    """

    session = SessionLocal()

    try:
        result = session.execute(
            text(
                """
                SELECT question, answer, timestamp
                FROM conversation_history
                WHERE user_id = :user_id
                  AND session_id = :session_id
                ORDER BY timestamp ASC, id ASC
                """
            ),
            {"user_id": user_id, "session_id": session_id},
        )

        return [dict(row) for row in result.mappings().all()]

    except Exception as exc:

        print(f"[DB] Failed to load session messages: {exc}", flush=True)
        return []

    finally:
        session.close()


# ==============================================================
# ANALYTICS / USAGE DASHBOARD
#
# All functions return pandas DataFrames (empty on error/no data)
# so the dashboard page can hand them straight to st.line_chart /
# st.bar_chart / st.dataframe without extra glue code.
# ==============================================================


def get_summary_stats(days: int = 30) -> Dict:
    """Headline numbers for the top of the dashboard."""

    session = SessionLocal()

    try:
        totals = session.execute(
            text(
                """
                SELECT
                    COUNT(*) AS total_queries,
                    COUNT(DISTINCT user_id) AS active_users,
                    COUNT(DISTINCT document_name) AS documents_used
                FROM conversation_history
                WHERE timestamp >= CURDATE() - INTERVAL :days DAY
                """
            ),
            {"days": days},
        ).mappings().first()

        perf = session.execute(
            text(
                """
                SELECT
                    ROUND(AVG(latency_ms), 0) AS avg_latency_ms,
                    ROUND(
                        100 * SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END)
                        / NULLIF(COUNT(*), 0),
                        1
                    ) AS success_rate
                FROM query_metrics
                WHERE timestamp >= CURDATE() - INTERVAL :days DAY
                """
            ),
            {"days": days},
        ).mappings().first()

        return {
            "total_queries": (totals["total_queries"] if totals else 0) or 0,
            "active_users": (totals["active_users"] if totals else 0) or 0,
            "documents_used": (totals["documents_used"] if totals else 0) or 0,
            "avg_latency_ms": (perf["avg_latency_ms"] if perf else 0) or 0,
            "success_rate": (perf["success_rate"] if perf else 0) or 0,
        }

    except Exception as exc:

        print(f"[DB] Failed to load summary stats: {exc}", flush=True)
        return {
            "total_queries": 0,
            "active_users": 0,
            "documents_used": 0,
            "avg_latency_ms": 0,
            "success_rate": 0,
        }

    finally:
        session.close()


def get_queries_per_day(days: int = 30) -> pd.DataFrame:
    """Daily query volume for the last N days, including zero-query days."""

    session = SessionLocal()

    try:
        result = session.execute(
            text(
                """
                SELECT
                    DATE(timestamp) AS query_date,
                    COUNT(*) AS total_queries
                FROM conversation_history
                WHERE timestamp >= CURDATE() - INTERVAL :days DAY
                GROUP BY DATE(timestamp)
                ORDER BY query_date
                """
            ),
            {"days": days},
        )

        df = pd.DataFrame(result.mappings().all())

        if df.empty:
            return df

        df["query_date"] = pd.to_datetime(df["query_date"])

        # Fill in gaps so the chart doesn't skip days with zero activity
        full_range = pd.date_range(
            df["query_date"].min(),
            df["query_date"].max(),
            freq="D",
        )

        df = (
            df.set_index("query_date")
            .reindex(full_range, fill_value=0)
            .rename_axis("query_date")
            .reset_index()
        )

        return df

    except Exception as exc:

        print(f"[DB] Failed to load queries per day: {exc}", flush=True)
        return pd.DataFrame()

    finally:
        session.close()


def get_latency_over_time(days: int = 30) -> pd.DataFrame:
    """Average latency per day, for spotting performance regressions."""

    session = SessionLocal()

    try:
        result = session.execute(
            text(
                """
                SELECT
                    DATE(timestamp) AS query_date,
                    ROUND(AVG(latency_ms), 0) AS avg_latency_ms
                FROM query_metrics
                WHERE timestamp >= CURDATE() - INTERVAL :days DAY
                GROUP BY DATE(timestamp)
                ORDER BY query_date
                """
            ),
            {"days": days},
        )

        return pd.DataFrame(result.mappings().all())

    except Exception as exc:

        print(f"[DB] Failed to load latency over time: {exc}", flush=True)
        return pd.DataFrame()

    finally:
        session.close()


def get_document_usage(days: int = 30) -> pd.DataFrame:
    """Which documents get queried most."""

    session = SessionLocal()

    try:
        result = session.execute(
            text(
                """
                SELECT
                    COALESCE(document_name, 'Unknown') AS document_name,
                    COUNT(*) AS total_queries
                FROM conversation_history
                WHERE timestamp >= CURDATE() - INTERVAL :days DAY
                GROUP BY document_name
                ORDER BY total_queries DESC
                LIMIT 15
                """
            ),
            {"days": days},
        )

        return pd.DataFrame(result.mappings().all())

    except Exception as exc:

        print(f"[DB] Failed to load document usage: {exc}", flush=True)
        return pd.DataFrame()

    finally:
        session.close()


def get_user_usage(days: int = 30) -> pd.DataFrame:
    """Per-user activity, joined against the users table."""

    session = SessionLocal()

    try:
        result = session.execute(
            text(
                """
                SELECT
                    u.id AS user_id,
                    u.name,
                    COUNT(ch.id) AS total_queries,
                    ROUND(AVG(qm.latency_ms), 0) AS avg_latency_ms
                FROM users u
                LEFT JOIN conversation_history ch
                    ON u.id = ch.user_id
                    AND ch.timestamp >= CURDATE() - INTERVAL :days DAY
                LEFT JOIN query_metrics qm
                    ON u.id = qm.user_id
                    AND qm.timestamp >= CURDATE() - INTERVAL :days DAY
                GROUP BY u.id, u.name
                ORDER BY total_queries DESC
                """
            ),
            {"days": days},
        )

        return pd.DataFrame(result.mappings().all())

    except Exception as exc:

        print(f"[DB] Failed to load user usage: {exc}", flush=True)
        return pd.DataFrame()

    finally:
        session.close()