# 🤖 AI PDF RAG Chatbot

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red?logo=streamlit)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Database-orange)](https://www.trychroma.com/)
[![RAG](https://img.shields.io/badge/Architecture-RAG-purple)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)

An intelligent document question-answering system that uses Retrieval-Augmented Generation (RAG) to understand and answer questions from PDF documents with context-aware responses.

## 📌 Overview

AI PDF RAG Chatbot is a document intelligence application that allows users to upload PDF documents and interact with them using natural language.

Instead of manually searching through large PDF documents, users can simply ask questions such as:

"What are the key concepts discussed in this document?"

The system retrieves the most relevant information from the uploaded documents and uses an LLM to generate a grounded response based on the retrieved context.

The project follows a modular Retrieval-Augmented Generation (RAG) architecture, combining:

📄 PDF processing
✂️ Intelligent text chunking
🧠 Embedding generation
🔎 Semantic search
🔤 BM25 keyword retrieval
🔀 Hybrid retrieval
🎯 Cross-encoder reranking
🤖 LLM-based generation
💬 Conversation memory
🖼️ Image retrieval
📊 Table retrieval
📐 Document layout detection
🗄️ MySQL-based query monitoring

## ⭐ Project Highlights

- Built an end-to-end Retrieval-Augmented Generation (RAG) pipeline for PDF question answering.
- Implemented semantic and BM25-based hybrid retrieval.
- Added cross-encoder reranking to improve retrieved context relevance.
- Integrated embedding-based vector search using ChromaDB.
- Implemented modular PDF processing, retrieval, reranking, LLM, memory, and database components.
- Added support for image and table retrieval.
- Integrated document layout analysis using DocLayout-YOLO.
- Exposed backend functionality through FastAPI.
- Built an interactive document-chat interface using Streamlit.
- Added query and latency monitoring capabilities using MySQL.
  
## 🚀 Why RAG?
Large Language Models can generate impressive answers, but they do not automatically know the contents of a user's private documents.

This project solves that problem using Retrieval-Augmented Generation.

Instead of sending an entire PDF to the LLM, the system:

PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
Vector Database
 ↓
User Question
 ↓
Relevant Document Retrieval
 ↓
Hybrid Search
 ↓
Reranking
 ↓
Relevant Context
 ↓
LLM
 ↓
Grounded Answer

This approach helps the chatbot provide answers based on the actual contents of the uploaded documents.

## ✨ Key Features

## 📄 1. PDF Document Processing

The system can process PDF documents and extract their contents for downstream retrieval.

Features include:

PDF text extraction
Page-level processing
Text cleaning
Intelligent chunking
Document metadata handling

## 🧠 2. Semantic Embeddings

Document chunks are converted into vector representations using:

BAAI/bge-small-en-v1.5

These embeddings allow the system to find content based on meaning, rather than only exact keyword matches.

For example:

Question:
"What is supervised learning?"

Relevant document:
"Supervised algorithms learn from labeled training examples..."

Even when the exact wording differs, semantic retrieval can identify the relevant content.

## 🔎 3. Hybrid Retrieval

One of the important parts of this project is the use of hybrid retrieval.

The system combines:

Semantic Search

Uses vector embeddings to understand the semantic meaning of the query.

BM25

Uses keyword-based retrieval to identify exact or highly relevant terms.

Hybrid Retrieval

Combines both approaches to improve retrieval quality.

                User Query
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
   Semantic Search          BM25
          │                   │
          └─────────┬─────────┘
                    ↓
             Hybrid Results

This provides a better balance between:

meaning-based retrieval + exact keyword matching

## 🎯 4. Cross-Encoder Reranking

After retrieving candidate documents, the system uses a cross-encoder to rerank the results.

Model:

cross-encoder/ms-marco-MiniLM-L-6-v2

The reranking stage helps prioritize the passages that are most relevant to the user's question before sending context to the LLM.

Initial Retrieval
       ↓
Candidate Passages
       ↓
Cross-Encoder
       ↓
Relevance Scoring
       ↓
Top Relevant Passages
       ↓
      LLM
      
## 🤖 5. LLM-Based Answer Generation

The retrieved document context is passed to an LLM to generate the final response.

The system is designed so that the LLM works with retrieved document context instead of relying only on its pretrained knowledge.

This makes the application suitable for document-based question answering.

## 💬 6. Conversation Memory

The chatbot includes conversation memory so users can ask follow-up questions naturally.

Example:

User:
What is machine learning?

Assistant:
Machine learning is...

User:
What are its main types?

Assistant:
The main types are...

The conversation context allows follow-up queries to remain meaningful.

## 🖼️ 7. Image & Table Retrieval

The project goes beyond plain text retrieval.

It includes modules for:

Image retrieval
Table retrieval
Extracted figures
Document structure analysis

This allows the architecture to be extended toward multimodal document understanding.

## 📐 8. Document Layout Detection

The project integrates DocLayout-YOLO for document layout analysis.

This can help identify document elements such as:

Text blocks
Images
Tables
Figures
Other structural components

This is particularly useful for PDFs where important information is not represented as simple linear text.

## 🗄️ 9. Database & Query Monitoring

The project also contains database components for monitoring application usage and performance.

The system can track information such as:

## Metric	                       Description
Query ID	                     Unique query identifier
User ID	                       User associated with query
Question	                     User's question
Retrieval Latency	             Time taken for retrieval
Generation Latency	           Time taken by the LLM
Total Latency                  Complete response time
Retrieved Chunks	             Number of retrieved chunks
Status	                       Query execution status
Created At	                   Query timestamp

These monitoring capabilities provide a foundation for evaluating and improving the system's performance during real-world usage.

## 🏗️ System Architecture
                         ┌─────────────────────┐
                         │       User          │
                         └──────────┬──────────┘
                                    │
                                    ↓
                         ┌─────────────────────┐
                         │  Streamlit UI       │
                         └──────────┬──────────┘
                                    │
                                    ↓
                         ┌─────────────────────┐
                         │     FastAPI         │
                         │      Backend        │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ↓                               ↓
          ┌──────────────────┐             ┌──────────────────┐
          │ PDF Processing   │             │ Conversation     │
          │ & Chunking       │             │ Memory           │
          └────────┬─────────┘             └──────────────────┘
                   │
                   ↓
          ┌──────────────────┐
          │ Embedding Model  │
          │ BGE-small-en     │
          └────────┬─────────┘
                   │
                   ↓
          ┌──────────────────┐
          │    ChromaDB      │
          │   Vector Store   │
          └────────┬─────────┘
                   │
                   ↓
        ┌─────────────────────────┐
        │    Hybrid Retrieval     │
        │                         │
        │ Semantic Search + BM25  │
        └────────────┬────────────┘
                     │
                     ↓
        ┌─────────────────────────┐
        │   Cross Encoder         │
        │      Reranker           │
        └────────────┬────────────┘
                     │
                     ↓
        ┌─────────────────────────┐
        │     Relevant Context    │
        └────────────┬────────────┘
                     │
                     ↓
        ┌─────────────────────────┐
        │          LLM            │
        │   Answer Generation     │
        └────────────┬────────────┘
                     │
                     ↓
        ┌─────────────────────────┐
        │     Final Response      │
        └─────────────────────────┘
## 🛠️ Tech Stack
## Programming
Python

## Backend
FastAPI
Uvicorn

## AI / ML
RAG
Sentence Transformers
BAAI/bge-small-en-v1.5
Cross-Encoder
DocLayout-YOLO
LLM API integration

## Retrieval
ChromaDB
BM25
Semantic Search
Hybrid Retrieval
Cross-Encoder Reranking

## PDF Processing
PyMuPDF
PDF text extraction
Image extraction
Document layout analysis

## Frontend
Streamlit

## Database
MySQL

## Development
Git
GitHub
VS Code
Postman

## 📂 Project Structure
AI-PDF-RAG-Chatbot/
│
├── data/
│   └── Sample PDF documents
│
├── database/
│   ├── connection.py
│   ├── crud.py
│   └── __init__.py
│
├── src/
│   ├── rag_pipeline.py
│   ├── pdf_loader.py
│   ├── text_splitter.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── reranker.py
│   ├── llm.py
│   ├── pdf_router.py
│   ├── image_retriever.py
│   ├── table_retriever.py
│   ├── layout_detector.py
│   ├── memory.py
│   ├── ocr.py
│   └── tools.py
│
├── DocLayout-YOLO/
│
├── ragflow-frontend/
│
├── tests/
│   └── test_pipeline_contract.py
│
├── api_server.py
├── app.py
├── frontend.py
├── debug_live_rag.py
├── test_mysql.py
├── requirements.txt
├── chroma_db_manifest.json
├── .gitignore
└── README.md

## ⚙️ Local Setup
## 1. Clone the repository
git clone https://github.com/Devanshivyas05/AI-PDF-RAG-Chatbot.git
cd AI-PDF-RAG-Chatbot

## 2. Create a virtual environment
## Windows
python -m venv venv
venv\Scripts\activate

## Linux / macOS
python3 -m venv venv
source venv/bin/activate

## 3. Install dependencies
pip install -r requirements.txt

## 🔐 Environment Configuration
Create a .env file in the project root.

Example:

GROQ_API_KEY=your_api_key_here

If database functionality is enabled, configure the required MySQL environment variables.

⚠️ Security: API keys, passwords, .env files, model weights, generated vector databases, and other sensitive/local artifacts should not be committed to GitHub.

## ▶️ Running the Application
## Start the FastAPI Backend
uvicorn api_server:app --reload

The backend will run at:

http://127.0.0.1:8000

Health check:

http://127.0.0.1:8000/health

## Start the Streamlit Frontend
streamlit run app.py

Depending on the selected frontend entry point, the application can also be started using:

streamlit run frontend.py

## 🧪 Testing

Run the test suite:

pytest

The repository contains tests for important components of the RAG pipeline.

## 📊 Example RAG Workflow

A typical user interaction follows this process:

1. Upload PDF
       ↓
2. Extract document content
       ↓
3. Split content into chunks
       ↓
4. Generate embeddings
       ↓
5. Store embeddings in ChromaDB
       ↓
6. User asks a question
       ↓
7. Perform semantic retrieval
       ↓
8. Perform BM25 retrieval
       ↓
9. Combine retrieval results
       ↓
10. Rerank candidate passages
       ↓
11. Build relevant context
       ↓
12. Send context to LLM
       ↓
13. Generate final response
    
## 💡 Example Use Cases

The architecture can be used for:

📚 Academic document Q&A
📑 Research paper analysis
🏢 Enterprise document assistants
📋 Policy and regulation search
📖 Study assistants
🧾 Technical documentation Q&A
🏥 Knowledge-base assistants
💼 Internal company document search

## 🎯 Engineering Highlights

This project demonstrates practical implementation of several modern AI engineering concepts:

## Retrieval-Augmented Generation

Building an end-to-end RAG pipeline instead of relying solely on an LLM.

## Vector Search

Converting documents into embeddings and performing similarity-based retrieval.

## Hybrid Search

Combining semantic retrieval with traditional keyword-based BM25 retrieval.

## Reranking

Using a cross-encoder to improve the relevance of retrieved context.

## Modular Architecture

Separating PDF processing, embeddings, retrieval, reranking, LLM interaction, memory, and database operations into dedicated modules.

## API Architecture

Using FastAPI to expose the backend functionality through APIs.

## Observability

Tracking retrieval and generation latency to understand application performance.

## 🚧 Current Limitations

The current implementation is primarily designed as an internship/project-level RAG system.

Some components may require additional configuration depending on the deployment environment, including:

LLM API credentials
MySQL configuration
Vector database persistence
Document layout model weights
CPU/GPU availability

## 🚀 Future Improvements

Planned improvements include:

 Cloud deployment
 User authentication and authorization
 Multi-user document isolation
 Streaming LLM responses
 Persistent cloud vector database
 Improved multimodal document understanding
 Advanced analytics dashboard
 Better document access control
 Asynchronous document processing
 Support for additional document formats
 
## 📸 Screenshots

Screenshots of the application will be added here after deployment.

## 🎥 Demo

Live Demo: Coming soon


## 👩‍💻 Author
Devanshi Vyas

GitHub:
https://github.com/Devanshivyas05

## ⭐ Project Summary

AI PDF RAG Chatbot demonstrates how modern Generative AI can be combined with traditional information retrieval techniques to build practical document intelligence applications.

The project combines:

PDF Processing
      +
Text Chunking
      +
Embeddings
      +
Vector Search
      +
BM25
      +
Hybrid Retrieval
      +
Cross-Encoder Reranking
      +
LLM
      +
Conversation Memory
      +
FastAPI
      +
Streamlit
      +
MySQL

to create an end-to-end AI-powered document question-answering system.

## ⭐ Built With

Python • RAG • FastAPI • ChromaDB • Streamlit • Sentence Transformers • BM25 • Cross-Encoder • MySQL • Generative AI.
