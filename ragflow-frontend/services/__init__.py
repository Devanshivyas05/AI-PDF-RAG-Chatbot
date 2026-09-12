"""Service layer connecting the Streamlit UI to the existing RAG backend."""

from .rag_service import RAGService, get_service, normalize_response

__all__ = ["RAGService", "get_service", "normalize_response"]
