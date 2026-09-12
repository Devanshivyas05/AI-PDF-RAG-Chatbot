import os
import traceback
from pathlib import Path
from threading import Lock
from typing import TYPE_CHECKING, Optional

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent
os.chdir(PROJECT_ROOT)
load_dotenv(PROJECT_ROOT / ".env")

# from fastapi import FastAPI
# from pydantic import BaseModel
# from langchain_chroma import Chroma
# from langchain_core.documents import Document
# from rank_bm25 import BM25Okapi

# from src.rag_pipeline import RAGPipeline

# app = FastAPI(title="PDF RAG API")

# _pipeline: Optional[RAGPipeline] = None


# class ChatRequest(BaseModel):
#     query: str


# def _load_existing_pipeline() -> RAGPipeline:
#     """Reuse the existing persisted ChromaDB/data index without re-ingesting PDFs."""
#     global _pipeline

#     if _pipeline is not None:
#         return _pipeline

#     pipeline = RAGPipeline()
#     chroma_dir = os.path.join(os.getcwd(), "chroma_db")

#     if not os.path.isdir(chroma_dir):
#         raise RuntimeError("Existing ChromaDB index not found. Please process PDFs before using the API.")

#     vector_db = Chroma(
#         persist_directory=chroma_dir,
#         embedding_function=pipeline.embedding_model,
#     )

#     results = vector_db.get(include=["documents", "metadatas"])
#     documents = results.get("documents", [])
#     metadatas = results.get("metadatas", [])

#     if not documents:
#         raise RuntimeError("No persisted documents found in the existing ChromaDB index.")

#     loaded_docs = []
#     for text, metadata in zip(documents, metadatas):
#         if not text:
#             continue
#         if metadata is None:
#             metadata = {}
#         loaded_docs.append(Document(page_content=text, metadata=dict(metadata)))

#     pipeline.vector_db = vector_db
#     pipeline.documents = loaded_docs
#     pipeline.bm25 = BM25Okapi([
#         doc.page_content.lower().split() for doc in loaded_docs if doc.page_content
#     ])
#     _pipeline = pipeline
#     return pipeline


# @app.get("/health")
# def health() -> dict:
#     return {"status": "ok"}


# @app.post("/chat")
# def chat(request: ChatRequest) -> dict:
#     query = (request.query or "").strip()
#     if not query:
#         return {"success": False, "error": "Query is required."}

#     try:
#         pipeline = _load_existing_pipeline()
#         answer = pipeline.ask(query)
#         if answer is None:
#             return {
#                 "success": False,
#                 "answer": "I couldn't find this information in the uploaded PDF.",
#                 "error": "No answer generated from existing context.",
#             }
#         return {"success": True, "answer": answer}
#     except Exception as exc:
#         return {
#             "success": False,
#             "answer": "I couldn't find this information in the uploaded PDF.",
#             "error": str(exc),
#         }


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=False)
from fastapi import FastAPI
from pydantic import BaseModel

if TYPE_CHECKING:
    from src.rag_pipeline import RAGPipeline

_pipeline: Optional["RAGPipeline"] = None
_pipeline_lock = Lock()


app = FastAPI(title="PDF RAG API")


class ChatRequest(BaseModel):
    query: str


def get_pipeline() -> "RAGPipeline":
    global _pipeline

    if _pipeline is not None:
        return _pipeline

    with _pipeline_lock:
        if _pipeline is None:
            from src.rag_pipeline import RAGPipeline

            print("\nRAG INITIALIZATION STARTED", flush=True)
            pipeline = RAGPipeline()

            data_folder = Path(
                os.environ.get("RAG_DATA_FOLDER", "data")
            )
            if not data_folder.is_absolute():
                data_folder = PROJECT_ROOT / data_folder

            if not data_folder.is_dir():
                raise RuntimeError(f"RAG data folder not found: {data_folder}")

            print(f"Processing PDFs from: {data_folder}")
            pipeline.process_pdf(str(data_folder))

            print(f"VECTOR DB: {pipeline.vector_db!r}", flush=True)
            print(f"BM25: {pipeline.bm25!r}", flush=True)
            if pipeline.vector_db is None or pipeline.bm25 is None:
                raise RuntimeError(
                    "RAG initialization completed without vector_db and bm25."
                )

            _pipeline = pipeline
            print("RAG INITIALIZATION COMPLETE", flush=True)

    return _pipeline


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    query = (request.query or "").strip()

    if not query:
        return {
            "success": False,
            "answer": "Query is required.",
            "error": "Empty query"
        }

    try:
        pipeline = get_pipeline()

        print("\n" + "=" * 80)
        print("API QUESTION:", query)
        print("=" * 80)

        answer = pipeline.ask(query)

        print("API ANSWER:", answer)
        print("=" * 80)

        if answer is None:
            return {
                "success": False,
                "answer": "I couldn't find this information in the uploaded PDF.",
                "error": "No answer generated from existing context."
            }

        return {
            "success": True,
            "answer": answer
        }

    except Exception as exc:
        print("RAG ERROR:", repr(exc), flush=True)
        traceback.print_exc()

        return {
            "success": False,
            "error": str(exc)
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )



import os
import sys
import time
import traceback
from contextlib import asynccontextmanager
from pathlib import Path
from threading import Lock
from typing import TYPE_CHECKING, Optional

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent
os.chdir(PROJECT_ROOT)
load_dotenv(PROJECT_ROOT / ".env")

# from fastapi import FastAPI
# from pydantic import BaseModel
# from langchain_chroma import Chroma
# from langchain_core.documents import Document
# from rank_bm25 import BM25Okapi

# from src.rag_pipeline import RAGPipeline

# app = FastAPI(title="PDF RAG API")

# _pipeline: Optional[RAGPipeline] = None


# class ChatRequest(BaseModel):
#     query: str


# def _load_existing_pipeline() -> RAGPipeline:
#     """Reuse the existing persisted ChromaDB/data index without re-ingesting PDFs."""
#     global _pipeline

#     if _pipeline is not None:
#         return _pipeline

#     pipeline = RAGPipeline()
#     chroma_dir = os.path.join(os.getcwd(), "chroma_db")

#     if not os.path.isdir(chroma_dir):
#         raise RuntimeError("Existing ChromaDB index not found. Please process PDFs before using the API.")

#     vector_db = Chroma(
#         persist_directory=chroma_dir,
#         embedding_function=pipeline.embedding_model,
#     )

#     results = vector_db.get(include=["documents", "metadatas"])
#     documents = results.get("documents", [])
#     metadatas = results.get("metadatas", [])

#     if not documents:
#         raise RuntimeError("No persisted documents found in the existing ChromaDB index.")

#     loaded_docs = []
#     for text, metadata in zip(documents, metadatas):
#         if not text:
#             continue
#         if metadata is None:
#             metadata = {}
#         loaded_docs.append(Document(page_content=text, metadata=dict(metadata)))

#     pipeline.vector_db = vector_db
#     pipeline.documents = loaded_docs
#     pipeline.bm25 = BM25Okapi([
#         doc.page_content.lower().split() for doc in loaded_docs if doc.page_content
#     ])
#     _pipeline = pipeline
#     return pipeline


# @app.get("/health")
# def health() -> dict:
#     return {"status": "ok"}


# @app.post("/chat")
# def chat(request: ChatRequest) -> dict:
#     query = (request.query or "").strip()
#     if not query:
#         return {"success": False, "error": "Query is required."}

#     try:
#         pipeline = _load_existing_pipeline()
#         answer = pipeline.ask(query)
#         if answer is None:
#             return {
#                 "success": False,
#                 "answer": "I couldn't find this information in the uploaded PDF.",
#                 "error": "No answer generated from existing context.",
#             }
#         return {"success": True, "answer": answer}
#     except Exception as exc:
#         return {
#             "success": False,
#             "answer": "I couldn't find this information in the uploaded PDF.",
#             "error": str(exc),
#         }


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=False)


from fastapi import FastAPI
from pydantic import BaseModel

if TYPE_CHECKING:
    from src.rag_pipeline import RAGPipeline

_pipeline: Optional["RAGPipeline"] = None
_pipeline_lock = Lock()

# Lifecycle state so /health and /chat can report reality instead of guessing.
# "starting" -> "ready" | "error"
_rag_state = {"status": "starting", "error": None}


def _log(msg: str) -> None:
    print(f"[API] {msg}", flush=True)


def _build_pipeline() -> "RAGPipeline":
    """Actual heavy construction. Runs exactly once, called from startup."""
    from src.rag_pipeline import RAGPipeline

    _log("INITIALIZING RAG PIPELINE")
    _log("CREATING RAGPipeline")
    pipeline = RAGPipeline()

    data_folder = Path(os.environ.get("RAG_DATA_FOLDER", "data"))
    if not data_folder.is_absolute():
        data_folder = PROJECT_ROOT / data_folder

    if not data_folder.is_dir():
        raise RuntimeError(f"RAG data folder not found: {data_folder}")

    _log(f"LOADING/PROCESSING DATA from: {data_folder}")
    pipeline.process_pdf(str(data_folder))

    _log(f"VECTOR DB: {pipeline.vector_db!r}")
    _log(f"BM25: {pipeline.bm25!r}")
    if pipeline.vector_db is None or pipeline.bm25 is None:
        raise RuntimeError("RAG initialization completed without vector_db and bm25.")

    _log("VECTOR DB READY")
    _log("BM25 READY")
    return pipeline


def get_pipeline() -> "RAGPipeline":
    """Return the already-initialized pipeline, or raise if not ready.

    Does NOT build the pipeline lazily anymore — that happens once at
    server startup via the lifespan handler below.
    """
    global _pipeline
    if _rag_state["status"] == "error":
        raise RuntimeError(f"RAG pipeline failed to initialize: {_rag_state['error']}")
    if _pipeline is None:
        raise RuntimeError("RAG pipeline is still initializing")
    return _pipeline


@asynccontextmanager
async def lifespan(app: "FastAPI"):
    global _pipeline
    _log("SERVER STARTED")
    try:
        with _pipeline_lock:
            start = time.time()
            _pipeline = _build_pipeline()
            _rag_state["status"] = "ready"
            _log(f"RAG PIPELINE READY ({time.time() - start:.1f}s)")
    except Exception as exc:
        _rag_state["status"] = "error"
        _rag_state["error"] = str(exc)
        _log("RAG INITIALIZATION FAILED")
        traceback.print_exc()
        # Do not raise: let the server come up so /health reports the real error
        # instead of the process refusing to start with no explanation.
    yield
    _log("SERVER SHUTTING DOWN")


app = FastAPI(title="PDF RAG API", lifespan=lifespan)


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "rag_ready": _rag_state["status"] == "ready",
        "rag_status": _rag_state["status"],
        "rag_error": _rag_state["error"],
    }


@app.post("/chat")
def chat(request: ChatRequest):
    query = (request.query or "").strip()

    if not query:
        return {
            "success": False,
            "answer": "Query is required.",
            "error": "Empty query"
        }

    _log("/chat REQUEST RECEIVED")
    _log(f"QUERY: {query}")

    if _rag_state["status"] == "starting":
        _log("REJECTED: pipeline still initializing")
        return {
            "success": False,
            "error": "RAG pipeline is still initializing",
        }

    if _rag_state["status"] == "error":
        _log("REJECTED: pipeline failed to initialize")
        return {
            "success": False,
            "error": f"RAG pipeline failed to initialize: {_rag_state['error']}",
        }

    try:
        pipeline = get_pipeline()

        _log("CALLING pipeline.ask()")
        answer = pipeline.ask(query)
        _log("pipeline.ask() RETURNED")

        if answer is None:
            _log("SENDING RESPONSE (no answer)")
            return {
                "success": False,
                "answer": "I couldn't find this information in the uploaded PDF.",
                "error": "No answer generated from existing context."
            }

        _log("SENDING RESPONSE")
        return {
            "success": True,
            "answer": answer
        }

    except Exception as exc:
        _log(f"RAG ERROR: {exc!r}")
        traceback.print_exc()

        return {
            "success": False,
            "error": str(exc)
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )