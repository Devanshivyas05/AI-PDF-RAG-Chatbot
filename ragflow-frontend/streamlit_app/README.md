# Enterprise Multi-PDF RAG — Streamlit Frontend

Frontend only. No RAG logic lives here.

## Run

```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

## Structure

```
streamlit_app/
├── app.py                 # page setup, state, layout orchestration
├── components/
│   ├── theme.py           # design system (fonts, tokens, CSS)
│   ├── sidebar.py         # knowledge base, stats, history, settings, pipeline
│   ├── chat.py            # transcript, bubbles, retrieval trace
│   ├── source_card.py     # citations + semantic/BM25/rerank score bars
│   ├── document_card.py   # PDF row with select/delete
│   ├── image_viewer.py    # YOLO-detected figures + OCR text
│   ├── table_viewer.py    # extracted tables + CSV export
│   ├── stats.py           # knowledge-base metrics
│   └── welcome.py         # empty state + pipeline flow
└── services/
    └── api.py             # ONLY place that talks to the backend
```

## Connect your existing backend

Edit nothing but `services/api.py`:

```bash
export RAG_USE_MOCK=false
export RAG_API_BASE_URL=http://localhost:8000
```

Expected endpoints:

| Method | Path | Returns |
| --- | --- | --- |
| GET | `/api/documents` | `[{id, filename, pages, status, size_label}]` |
| POST | `/api/documents` | uploaded document (multipart field `file`) |
| DELETE | `/api/documents/{id}` | `{ok: true}` |
| GET | `/api/documents/stats` | `{pdfs, pages, images, tables, chunks}` |
| POST | `/api/chat` | assistant message (see below) |
| GET | `/api/sources/{id}` | source chunk |
| GET | `/api/images/{id}` | image bytes |
| GET | `/api/tables/{id}` | table |
| GET | `/api/history` | `[{id, title, updated_at}]` |

Assistant message shape:

```json
{
  "id": "…", "role": "assistant", "content": "markdown", "created_at": 0,
  "sources": [{"id","document_id","filename","page","chunk","relevance",
               "scores":{"semantic","bm25","rerank"}}],
  "figures": [{"id","url","caption","filename","page","detected_by","ocr_text"}],
  "tables":  [{"id","filename","page","title","columns","rows"}],
  "trace":   [{"key","label","detail"}]
}
```

Alternatively, replace the function bodies in `services/api.py` with direct
calls into your Python pipeline — the UI never needs to change.
