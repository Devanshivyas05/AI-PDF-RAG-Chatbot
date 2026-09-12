"""
API SERVICE ABSTRACTION
=======================
>>> THIS IS THE ONLY FILE YOU NEED TO EDIT TO CONNECT YOUR PYTHON RAG BACKEND <<<

The Streamlit UI talks to the backend *exclusively* through `api` below.
Right now it returns mock data so the frontend can be developed standalone.

Set USE_MOCK = False (or env RAG_USE_MOCK=false) and point API_BASE_URL at your
FastAPI/Flask server -- or simply replace the bodies of these functions with
direct calls into your existing RAG pipeline (import it, don't rewrite it).

Expected HTTP contract:
    GET    {BASE}/api/documents          -> list[Document]
    POST   {BASE}/api/documents          -> Document        (multipart "file")
    DELETE {BASE}/api/documents/{id}     -> {"ok": true}
    GET    {BASE}/api/documents/stats    -> Stats
    POST   {BASE}/api/chat               -> AssistantMessage
    GET    {BASE}/api/sources/{id}       -> Source
    GET    {BASE}/api/images/{id}        -> image bytes
    GET    {BASE}/api/tables/{id}        -> Table
    GET    {BASE}/api/history            -> list[Thread]
"""

from __future__ import annotations

import os
import time
import uuid
from typing import Any, Dict, List, Optional

import requests

API_BASE_URL = os.getenv("RAG_API_BASE_URL", "http://localhost:8000")
USE_MOCK = os.getenv("RAG_USE_MOCK", "true").lower() != "false"
TIMEOUT = 120


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------
def _request(method: str, path: str, **kwargs) -> Any:
    res = requests.request(method, f"{API_BASE_URL}{path}", timeout=TIMEOUT, **kwargs)
    if not res.ok:
        raise RuntimeError(f"Backend error {res.status_code}: {res.text[:300]}")
    return res.json()


# ---------------------------------------------------------------------------
# Mock layer (frontend development only -- never real RAG logic)
# ---------------------------------------------------------------------------
_MOCK_DOCS: List[Dict[str, Any]] = [
    {"id": "doc-1", "filename": "deep_learning_textbook.pdf", "pages": 412,
     "status": "ready", "size_label": "18.4 MB"},
    {"id": "doc-2", "filename": "transformer_architectures.pdf", "pages": 96,
     "status": "ready", "size_label": "4.1 MB"},
    {"id": "doc-3", "filename": "annual_compliance_report.pdf", "pages": 148,
     "status": "ready", "size_label": "7.9 MB"},
]

_MOCK_THREADS = [
    {"id": "t1", "title": "CNN architecture overview", "updated_at": time.time() - 3600},
    {"id": "t2", "title": "Compare optimizer results", "updated_at": time.time() - 7200},
    {"id": "t3", "title": "Compliance risk summary", "updated_at": time.time() - 200000},
]


def _mock_sources(doc_ids: List[str]) -> List[Dict[str, Any]]:
    docs = [d for d in _MOCK_DOCS if not doc_ids or d["id"] in doc_ids] or _MOCK_DOCS
    out = []
    for i, d in enumerate(docs[:3]):
        rerank = round(0.94 - i * 0.11, 3)
        out.append({
            "id": f"src-{d['id']}-{i}",
            "document_id": d["id"],
            "filename": d["filename"],
            "page": 24 + i * 13,
            "chunk": (
                "Convolutional layers apply learned filters across the input volume, "
                "producing feature maps that progressively encode higher-level structure. "
                "Pooling reduces spatial resolution while retaining the strongest activations, "
                "which keeps the representation translation tolerant."
            ),
            "relevance": rerank,
            "scores": {
                "semantic": round(0.88 - i * 0.09, 3),
                "bm25": round(0.71 - i * 0.12, 3),
                "rerank": rerank,
            },
        })
    return out


def _mock_answer(message: str, doc_ids: List[str]) -> Dict[str, Any]:
    time.sleep(1.1)
    lower = message.lower()
    figures, tables = [], []

    if any(k in lower for k in ("diagram", "image", "figure", "architecture", "show")):
        figures = [{
            "id": "fig-1",
            "url": f"{API_BASE_URL}/api/images/fig-1",
            "caption": "Figure 4.2 — CNN architecture: convolution, pooling and dense stages.",
            "filename": _MOCK_DOCS[0]["filename"],
            "page": 137,
            "detected_by": "YOLO",
            "ocr_text": "INPUT → CONV → POOL → CONV → POOL → FC → SOFTMAX",
        }]

    if any(k in lower for k in ("table", "compare", "comparison", "benchmark", "results")):
        tables = [{
            "id": "tbl-1",
            "filename": _MOCK_DOCS[1]["filename"],
            "page": 58,
            "title": "Table 3.1 — Optimizer comparison on the validation split",
            "columns": ["Optimizer", "Top-1 Acc.", "Epochs", "Wall clock"],
            "rows": [
                ["SGD + momentum", "74.2%", "90", "6h 12m"],
                ["Adam", "76.8%", "60", "4h 05m"],
                ["AdamW", "78.1%", "60", "4h 11m"],
                ["LAMB", "77.4%", "45", "3h 22m"],
            ],
        }]

    body = (
        f"**Answer synthesised from {max(len(doc_ids), 1)} selected document(s).**\n\n"
        "The retrieved passages describe a staged pipeline in which convolutional blocks "
        "extract local features, pooling compresses spatial detail, and fully connected "
        "layers map the resulting representation onto class logits.\n\n"
        "Key points grounded in the sources:\n\n"
        "- Early layers respond to edges and textures; deeper layers encode object parts.\n"
        "- Pooling provides translation tolerance and reduces parameter count.\n"
        "- Normalisation and residual connections stabilise optimisation at depth.\n\n"
        "> Every claim above maps to a cited chunk listed under **Sources**."
    )

    return {
        "id": str(uuid.uuid4()),
        "role": "assistant",
        "content": body,
        "created_at": time.time(),
        "sources": _mock_sources(doc_ids),
        "figures": figures,
        "tables": tables,
        "trace": [
            {"key": "route", "label": "Document routing", "detail": f"{max(len(doc_ids),1)} PDFs"},
            {"key": "semantic", "label": "Semantic search (ChromaDB)", "detail": "top 20"},
            {"key": "bm25", "label": "Keyword search (BM25)", "detail": "top 20"},
            {"key": "fuse", "label": "Hybrid fusion", "detail": "28 candidates"},
            {"key": "rerank", "label": "CrossEncoder reranking", "detail": "top 3"},
            {"key": "generate", "label": "Answer generation (Groq)", "detail": "grounded"},
        ],
    }


# ---------------------------------------------------------------------------
# Public API used by the UI
# ---------------------------------------------------------------------------
class RagApi:
    # -- documents ---------------------------------------------------------
    def list_documents(self) -> List[Dict[str, Any]]:
        if USE_MOCK:
            return list(_MOCK_DOCS)
        return _request("GET", "/api/documents")

    def upload_document(self, filename: str, data: bytes) -> Dict[str, Any]:
        if USE_MOCK:
            time.sleep(0.8)
            doc = {
                "id": f"doc-{uuid.uuid4().hex[:6]}",
                "filename": filename,
                "pages": 42,
                "status": "ready",
                "size_label": f"{len(data) / 1_048_576:.1f} MB",
            }
            _MOCK_DOCS.append(doc)
            return doc
        return _request(
            "POST", "/api/documents",
            files={"file": (filename, data, "application/pdf")},
        )

    def delete_document(self, doc_id: str) -> Dict[str, Any]:
        if USE_MOCK:
            global _MOCK_DOCS
            _MOCK_DOCS[:] = [d for d in _MOCK_DOCS if d["id"] != doc_id]
            return {"ok": True}
        return _request("DELETE", f"/api/documents/{doc_id}")

    def stats(self) -> Dict[str, int]:
        if USE_MOCK:
            pages = sum(d["pages"] for d in _MOCK_DOCS)
            return {
                "pdfs": len(_MOCK_DOCS),
                "pages": pages,
                "images": max(0, pages // 12),
                "tables": max(0, pages // 25),
                "chunks": pages * 7,
            }
        return _request("GET", "/api/documents/stats")

    # -- chat --------------------------------------------------------------
    def send_message(
        self,
        message: str,
        document_ids: List[str],
        thread_id: Optional[str] = None,
        response_style: str = "detailed",
    ) -> Dict[str, Any]:
        if USE_MOCK:
            return _mock_answer(message, document_ids)
        return _request("POST", "/api/chat", json={
            "message": message,
            "document_ids": document_ids,
            "thread_id": thread_id,
            "response_style": response_style,
        })

    # -- artefacts ---------------------------------------------------------
    def get_source(self, source_id: str) -> Dict[str, Any]:
        if USE_MOCK:
            return _mock_sources([])[0]
        return _request("GET", f"/api/sources/{source_id}")

    def get_table(self, table_id: str) -> Dict[str, Any]:
        if USE_MOCK:
            return _mock_answer("table", [])["tables"][0]
        return _request("GET", f"/api/tables/{table_id}")

    def image_url(self, image_id: str) -> str:
        return f"{API_BASE_URL}/api/images/{image_id}"

    def history(self) -> List[Dict[str, Any]]:
        if USE_MOCK:
            return list(_MOCK_THREADS)
        return _request("GET", "/api/history")

    def health(self) -> bool:
        if USE_MOCK:
            return True
        try:
            requests.get(f"{API_BASE_URL}/health", timeout=3)
            return True
        except Exception:
            return False


api = RagApi()
