# """
# Thin connector between the Streamlit UI and the EXISTING RAG backend.

# This layer contains NO retrieval, embedding, reranking, YOLO, OCR or LLM logic.
# All of that already lives in src/rag_pipeline.py and its modules.
# Its only job: import the pipeline, call it safely, and normalise the response
# shape for the UI.
# """

# from __future__ import annotations

# import os
# from dataclasses import dataclass, field
# from typing import Any, Dict, List, Optional

# import requests


# DATA_FOLDER = os.environ.get("RAG_DATA_FOLDER", "data")
# API_BASE_URL = os.environ.get("RAG_API_URL", "http://127.0.0.1:8000")


# class BackendUnavailable(RuntimeError):
#     """Raised when the existing RAG backend cannot be imported/initialised."""


# @dataclass
# class RAGService:
#     """Adapter around src.rag_pipeline.RAGPipeline."""

#     data_folder: str = DATA_FOLDER
#     pipeline: Any = None
#     ready: bool = False
#     error: Optional[str] = None
#     _processed: List[str] = field(default_factory=list)

#     # -- lifecycle ---------------------------------------------------------
#     def initialize(self, data_folder: Optional[str] = None) -> bool:
#         """Check whether the FastAPI backend is available, without re-indexing PDFs."""
#         folder = data_folder or self.data_folder
#         self.data_folder = folder

#         try:
#             response = requests.get(f"{API_BASE_URL}/health", timeout=5)
#             if response.status_code != 200:
#                 self.error = "RAG backend is not running."
#                 self.ready = False
#                 return False
#         except requests.RequestException:
#             self.error = "RAG backend is not running."
#             self.ready = False
#             return False

#         self.ready = True
#         self.error = None
#         self._processed = self.list_pdfs()
#         return True

#     # -- documents ---------------------------------------------------------
#     def list_pdfs(self) -> List[str]:
#         """Dynamically discover PDFs in the configured data folder."""
#         try:
#             return sorted(
#                 f for f in os.listdir(self.data_folder) if f.lower().endswith(".pdf")
#             )
#         except Exception:
#             return []

#     def save_uploaded_pdf(self, filename: str, content: bytes) -> str:
#         """Persist an uploaded PDF into the data folder and re-index via backend."""
#         os.makedirs(self.data_folder, exist_ok=True)
#         path = os.path.join(self.data_folder, os.path.basename(filename))
#         with open(path, "wb") as fh:
#             fh.write(content)
#         if self.pipeline is not None:
#             try:
#                 self.pipeline.process_pdf(self.data_folder)
#             except Exception as exc:
#                 self.error = f"Re-indexing failed: {exc}"
#         return path

#     def stats(self) -> Dict[str, Any]:
#         return {
#             "documents": len(self.list_pdfs()),
#             "retrieval": "Hybrid",
#             "embeddings": "BGE",
#             "llm": "Groq",
#         }

#     # -- query -------------------------------------------------------------
#     def ask(self, question: str) -> Dict[str, Any]:
#         """Send the question to the FastAPI backend and normalise the response."""
#         if not self.ready:
#             return {
#                 "answer": None,
#                 "error": self.error or "RAG backend is not running.",
#             }

#         try:
#             response = requests.post(
#                 f"{API_BASE_URL}/chat",
#                 json={"query": question},
#                 timeout=1800,
#             )
#             if response.status_code != 200:
#                 return {
#                     "answer": None,
#                     "error": f"Backend returned HTTP {response.status_code}: {response.text}",
#                 }

#             payload = response.json()
#             if not payload.get("success", False):
#                 return {
#                     "answer": payload.get("answer") or "I couldn't find this information in the uploaded PDF.",
#                     "error": payload.get("error") or "Backend error.",
#                 }

#             return {"answer": payload.get("answer"), "error": None}
#         except requests.RequestException as exc:
#             return {"answer": None, "error": f"Backend request failed: {exc}"}
#         except ValueError:
#             return {"answer": None, "error": "Backend returned an invalid response."}


# def normalize_response(raw: Any) -> Dict[str, Any]:
#     """Accept whatever the backend returns and expose a predictable dict.

#     Recognised (all optional): answer, image, table, page, pdf, ocr_text,
#     page_image, sources.
#     """
#     if raw is None:
#         return {"answer": None}
#     if isinstance(raw, str):
#         return {"answer": raw}
#     if not isinstance(raw, dict):
#         return {"answer": str(raw)}

#     out: Dict[str, Any] = {
#         "answer": raw.get("answer") or raw.get("response") or raw.get("result"),
#         "image": raw.get("image") or raw.get("image_path") or raw.get("figure"),
#         "table": raw.get("table"),
#         "page": raw.get("page"),
#         "pdf": raw.get("pdf") or raw.get("source") or raw.get("document"),
#         "ocr_text": raw.get("ocr_text") or raw.get("ocr"),
#         "page_image": raw.get("page_image") or raw.get("page_preview"),
#         "sources": raw.get("sources") or [],
#         "error": raw.get("error"),
#     }
#     return {k: v for k, v in out.items() if v not in (None, "", [], {})}


# _service: Optional[RAGService] = None


# def get_service(data_folder: Optional[str] = None) -> RAGService:
#     """Process-wide singleton so the heavy pipeline is built only once."""
#     global _service
#     if _service is None:
#         _service = RAGService(data_folder=data_folder or DATA_FOLDER)
#     return _service




"""
Thin connector between the Streamlit UI and the EXISTING RAG backend.

This layer contains NO retrieval, embedding, reranking, YOLO, OCR or LLM logic.
All of that already lives in src/rag_pipeline.py and its modules.
Its only job: import the pipeline, call it safely, and normalise the response
shape for the UI.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import requests


DATA_FOLDER = os.environ.get("RAG_DATA_FOLDER", "data")
API_BASE_URL = os.environ.get("RAG_API_URL", "http://127.0.0.1:8000")


def _log(msg: str) -> None:
    print(f"[SERVICE] {msg}", flush=True)


class BackendUnavailable(RuntimeError):
    """Raised when the existing RAG backend cannot be imported/initialised."""


@dataclass
class RAGService:
    """Adapter around src.rag_pipeline.RAGPipeline."""

    data_folder: str = DATA_FOLDER
    pipeline: Any = None
    ready: bool = False
    error: Optional[str] = None
    _processed: List[str] = field(default_factory=list)

    # -- lifecycle ---------------------------------------------------------
    def initialize(self, data_folder: Optional[str] = None) -> bool:
        """Check whether the FastAPI backend is available, without re-indexing PDFs."""
        folder = data_folder or self.data_folder
        self.data_folder = folder

        _log("Checking backend health")
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            _log(f"HTTP status = {response.status_code}")
            if response.status_code != 200:
                self.error = "RAG backend is not running."
                self.ready = False
                return False

            payload = response.json()
            rag_ready = payload.get("rag_ready", False)
            rag_status = payload.get("rag_status", "unknown")
            _log(f"Backend health OK, rag_ready={rag_ready}, rag_status={rag_status}")

            if not rag_ready:
                self.error = payload.get("rag_error") or f"RAG backend not ready yet (status={rag_status})."
                self.ready = False
                return False

        except requests.RequestException as exc:
            _log(f"Health check failed: {exc}")
            self.error = "RAG backend is not running."
            self.ready = False
            return False

        self.ready = True
        self.error = None
        self._processed = self.list_pdfs()
        return True

    # -- documents ---------------------------------------------------------
    def list_pdfs(self) -> List[str]:
        """Dynamically discover PDFs in the configured data folder."""
        try:
            return sorted(
                f for f in os.listdir(self.data_folder) if f.lower().endswith(".pdf")
            )
        except Exception:
            return []

    def save_uploaded_pdf(self, filename: str, content: bytes) -> str:
        """Persist an uploaded PDF into the data folder and re-index via backend."""
        os.makedirs(self.data_folder, exist_ok=True)
        path = os.path.join(self.data_folder, os.path.basename(filename))
        with open(path, "wb") as fh:
            fh.write(content)
        if self.pipeline is not None:
            try:
                self.pipeline.process_pdf(self.data_folder)
            except Exception as exc:
                self.error = f"Re-indexing failed: {exc}"
        return path

    def stats(self) -> Dict[str, Any]:
        return {
            "documents": len(self.list_pdfs()),
            "retrieval": "Hybrid",
            "embeddings": "BGE",
            "llm": "Groq",
        }

    # -- query -------------------------------------------------------------
    def ask(self, question: str) -> Dict[str, Any]:
        """Send the question to the FastAPI backend and normalise the response."""
        if not self.ready:
            return {
                "answer": None,
                "error": self.error or "RAG backend is not running.",
            }

        _log("Sending POST /chat")
        try:
            response = requests.post(
                f"{API_BASE_URL}/chat",
                json={"query": question},
                timeout=1800,
            )
            _log(f"Response received, HTTP status = {response.status_code}")
            if response.status_code != 200:
                return {
                    "answer": None,
                    "error": f"Backend returned HTTP {response.status_code}: {response.text}",
                }

            payload = response.json()
            if not payload.get("success", False):
                _log(f"Backend reported failure: {payload.get('error')}")
                return {
                    "answer": payload.get("answer") or "I couldn't find this information in the uploaded PDF.",
                    "error": payload.get("error") or "Backend error.",
                }

            _log("Backend reported success")
            return {"answer": payload.get("answer"), "error": None}
        except requests.RequestException as exc:
            _log(f"Request failed: {exc}")
            return {"answer": None, "error": f"Backend request failed: {exc}"}
        except ValueError:
            _log("Backend returned invalid JSON")
            return {"answer": None, "error": "Backend returned an invalid response."}


def normalize_response(raw: Any) -> Dict[str, Any]:
    """Accept whatever the backend returns and expose a predictable dict.

    Recognised (all optional): answer, image, table, page, pdf, ocr_text,
    page_image, sources.
    """
    if raw is None:
        return {"answer": None}
    if isinstance(raw, str):
        return {"answer": raw}
    if not isinstance(raw, dict):
        return {"answer": str(raw)}

    out: Dict[str, Any] = {
        "answer": raw.get("answer") or raw.get("response") or raw.get("result"),
        "image": raw.get("image") or raw.get("image_path") or raw.get("figure"),
        "table": raw.get("table"),
        "page": raw.get("page"),
        "pdf": raw.get("pdf") or raw.get("source") or raw.get("document"),
        "ocr_text": raw.get("ocr_text") or raw.get("ocr"),
        "page_image": raw.get("page_image") or raw.get("page_preview"),
        "sources": raw.get("sources") or [],
        "error": raw.get("error"),
    }
    return {k: v for k, v in out.items() if v not in (None, "", [], {})}


_service: Optional[RAGService] = None


def get_service(data_folder: Optional[str] = None) -> RAGService:
    """Process-wide singleton so the heavy pipeline is built only once."""
    global _service
    if _service is None:
        _service = RAGService(data_folder=data_folder or DATA_FOLDER)
    return _service

