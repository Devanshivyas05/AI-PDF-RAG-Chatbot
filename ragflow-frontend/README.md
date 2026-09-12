# RAGFlow — Streamlit Frontend for your PDF RAG Chatbot

A premium, dark-themed Streamlit frontend for an enterprise Multi-PDF RAG
chatbot. This folder is the **frontend only** — it contains **no RAG logic**.
All retrieval, embedding, reranking, LLM, image/table/OCR work is delegated to
your existing Python RAG pipeline.

> Built with **Streamlit + Python only** (no React / Vite / Node.js).
> Designed to plug into an existing backend with modules such as
> `rag_pipeline.py`, `pdf_loader.py`, `text_splitter.py`, `embeddings.py`,
> `vector_store.py`, `retriever.py`, `reranker.py`, `llm.py`, `pdf_router.py`,
> `memory.py`, `tools.py`, `image_retriever.py`, `table_retriever.py`,
> `layout_detector.py`, `ocr.py`.

---

## 1. What's in this folder

```
ragflow-frontend/
├── frontend.py              ← MAIN APP ENTRY (premium RAGFlow UI). Run this one.
├── frontend/                ← UI package for frontend.py
│   ├── __init__.py
│   ├── styles.py             (dark navy theme, Streamlit chrome hidden)
│   ├── sidebar.py            (brand, dynamic PDF discovery + selection, AI pipeline chips)
│   ├── components.py         (header, hero, stats, status panel, examples, errors)
│   ├── chat.py               (user/assistant transcript rendering)
│   └── source_viewer.py     (source card, image/figure, table, page preview)
├── services/                ← thin connector to YOUR backend
│   ├── __init__.py
│   └── rag_service.py        (RAGService adapter around src.rag_pipeline.RAGPipeline)
├── requirements.txt
├── README.md                ← (this file)
└── streamlit_app/           ← ALTERNATE modular app (optional, uses HTTP API service)
    ├── app.py
    ├── README.md
    ├── requirements.txt
    ├── components/  (chat, sidebar, source_card, document_card, image_viewer,
    │                 table_viewer, stats, welcome, theme)
    └── services/api.py       (HTTP client + mock data; set RAG_USE_MOCK=false to go live)
```

**Two frontends are included:**

| App | Entry | How it talks to the backend | Use when |
|-----|-------|------------------------------|----------|
| **RAGFlow (primary)** | `frontend.py` | Imports `src.rag_pipeline.RAGPipeline` directly (in-process) | Your pipeline runs in the same Python process — simplest, recommended |
| streamlit_app (alternate) | `streamlit_app/app.py` | Calls a REST API (`requests`) with a mock fallback | Your pipeline is exposed as a FastAPI/Flask HTTP server |

You only need to run **one** of them. Use `frontend.py` unless you already run
your backend as a separate HTTP server.

---

## 2. Quick start (Windows)

Requires **Python 3.10+** (3.11 recommended).

```bat
:: 1. Open a terminal (PowerShell or cmd) in THIS folder
cd "C:\path\to\ragflow-frontend"

:: 2. (recommended) create & activate a virtual environment
python -m venv .venv
.venv\Scripts\activate

:: 3. install the frontend dependencies
pip install -r requirements.txt

:: 4. run the frontend
streamlit run frontend.py
```

Streamlit will open `http://localhost:8501` in your browser.

### Alternate app (HTTP-API version)

```bat
pip install -r streamlit_app\requirements.txt
streamlit run streamlit_app\app.py
```

---

## 3. Where to place this folder relative to your backend

Your backend expects the pipeline module at import path `src.rag_pipeline`
(that is the existing `from src.rag_pipeline import RAGPipeline` import in
`services/rag_service.py`). Two easy options:

**Option A — recommended (side-by-side):**
Place this `ragflow-frontend` folder **next to** your backend's `src/` folder:

```
your-project/
├── src/                     ← your existing RAG backend
│   ├── rag_pipeline.py
│   ├── retriever.py
│   ├── ... (all your backend modules)
│   └── __init__.py
└── ragflow-frontend/         ← THIS folder
    ├── frontend.py
    ├── services/rag_service.py   ← imports `from src.rag_pipeline import RAGPipeline`
    └── ...
```

Then run `streamlit run frontend.py` from the `your-project` root (so that
`src` is importable), OR run from inside `ragflow-frontend` after adding the
parent dir to the Python path (see step 4).

**Option B — inside your project root:**
If your existing `src/` already lives at the repo root, just drop this folder
anywhere under the repo root and run Streamlit from the repo root:

```bat
cd your-project
streamlit run ragflow-frontend\frontend.py
```

Running from the repo root makes `src.rag_pipeline` importable automatically.

---

## 4. Connect the frontend to your existing RAGPipeline class

**Edit one file: `services/rag_service.py`** (the only file that touches your
backend). It already does the right thing if your pipeline matches the assumed
shape — review and adjust the two spots below:

1. **The import + constructor** (`initialize()`):
   ```python
   from src.rag_pipeline import RAGPipeline   # adjust if your path differs
   self.pipeline = RAGPipeline()              # pass config if your class needs it
   ```

2. **The two calls** the frontend makes on your pipeline:
   - `self.pipeline.process_pdf(folder)` — index a folder of PDFs.
   - `self.pipeline.ask(question)` — return the answer + metadata.

   The frontend reads the returned dict through `normalize_response()`, which
   already accepts these **optional** keys (provide whichever your pipeline
   returns; the rest degrade gracefully):
   - `answer` (or `response` / `result`) — the generated text
   - `image` (or `image_path` / `figure`) — bytes / path / URL of a detected figure
   - `table` — DataFrame / list / dict / CSV path of an extracted table
   - `page` — page number of the answer/source
   - `pdf` (or `source` / `document`) — source PDF name
   - `ocr_text` (or `ocr`) — OCR text for a figure
   - `page_image` (or `page_preview`) — rendered source page image
   - `sources` — list of retrieved chunks
   - `error` — backend error string (optional)

If your `RAGPipeline.ask()` returns a different dict shape, just map it in
`normalize_response()` — **no UI code needs to change.**

---

## 5. Environment variables

All optional. Defaults work for local, in-process use with `frontend.py`.

| Variable | Default | Purpose |
|----------|---------|---------|
| `RAG_DATA_FOLDER` | `data` | Folder scanned for PDFs (relative or absolute path) |
| `RAG_USE_MOCK` | `true` | Only used by the **alternate** `streamlit_app`. Set `false` to call your HTTP API |
| `RAG_API_BASE_URL` | `http://localhost:8000` | Only used by the alternate `streamlit_app` when `RAG_USE_MOCK=false` |

For the **primary** `frontend.py`, you usually only set:

```bat
set RAG_DATA_FOLDER=C:\path\to\your\pdfs
```

If your pipeline reads keys (e.g. Groq) from the environment, export those too
— the frontend passes them through unchanged (they're read by your backend).

---

## 6. Dependency list (requirements.txt)

```text
streamlit>=1.36
pandas>=2.0
pillow>=10.0
```

The alternate `streamlit_app/requirements.txt` adds `requests`:

```text
streamlit>=1.36
requests>=2.31
pandas>=2.0
```

Your backend's own dependencies (ChromaDB, BGE, CrossEncoder, Groq, YOLO, OCR,
etc.) are **not** listed here — install them in the same environment as your
existing pipeline. This folder only ships the **frontend** dependencies.

---

## 7. The full data flow

```
Streamlit UI (frontend.py)
   │  user asks a question
   ▼
services/rag_service.py  (RAGService.ask)
   │  normalize the request
   ▼
src.rag_pipeline.RAGPipeline.ask(question)   ← YOUR existing backend
   │
   ├─ pdf_router.py      (route to relevant PDFs)
   ├─ retriever.py        (semantic + BM25 hybrid retrieval)
   ├─ reranker.py         (CrossEncoder reranking)
   ├─ llm.py              (Groq)  → answer
   ├─ image_retriever.py → image/figure  (+ ocr.py OCR text)
   ├─ table_retriever.py → table
   └─ metadata: pdf, page, image/table paths, OCR text
   ▼
normalize_response()  →  {answer, image, table, page, pdf, ocr_text, sources, ...}
   ▼
Streamlit UI renders: answer (markdown) + source card + image viewer
                     + table viewer + page preview
```

---

## 8. UI features (already built — do not change)

- Dark professional theme (navy surfaces, blue/purple accents)
- Modern AI/product-style interface, professional typography, clean spacing
- Sidebar: RAGFlow brand, dynamic PDF discovery + selection, AI Pipeline chips
- Main chat interface with example prompts
- Document/source information cards (PDF + page + content type badges)
- Retrieval / RAG pipeline status panel (routing → retrieval → reranking → answer)
- Image/figure viewer (YOLO-detected figures) with optional OCR text
- Table viewer (DataFrame with CSV download)
- Responsive layout, graceful handling of missing fields (no tracebacks)

---

## 9. Troubleshooting

- **`ModuleNotFoundError: No module named 'src'`** — you ran `frontend.py` from
  inside `ragflow-frontend/` but `src/` isn't on the path. Either run from the
  repo root (`streamlit run ragflow-frontend\frontend.py`), or add the parent
  dir: `set PYTHONPATH=..` before running, or move `src/`'s parent onto the path.
- **Backend not available / "RAG backend not available"** — your pipeline
  modules or their deps (ChromaDB, BGE, Groq, etc.) aren't importable in this
  environment. Install your backend's requirements in the same venv.
- **No PDFs showing** — set `RAG_DATA_FOLDER` to a folder containing `.pdf`
  files, or drop PDFs into the default `data/` folder.
- **Image/table not rendering** — your `ask()` didn't return `image`/`table`
  keys for that query; the UI shows the answer and sources without them.

---

Frontend only. Your existing RAG pipeline is untouched.
