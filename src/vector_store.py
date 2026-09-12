# from langchain_chroma import Chroma
# from rank_bm25 import BM25Okapi
# import shutil
# import os


# def create_vector_store(documents, embedding_model):
#     """
#     Creates:

#     1. ChromaDB (Semantic Search)
#     2. BM25 Index

#     ChromaDB only supports primitive metadata types,
#     so we store only simple metadata there.
#     """

#     print("\n🔄 Converting Chunks into Embeddings...\n")

#     texts = []

#     metadatas = []

#     # ------------------------------------------
#     # Delete old ChromaDB
#     # ------------------------------------------

#     if os.path.exists("chroma_db"):

#         shutil.rmtree("chroma_db")

#         print("🗑 Old ChromaDB Deleted")

#     # ------------------------------------------
#     # Prepare Data
#     # ------------------------------------------

#     for i, doc in enumerate(documents, start=1):

#         texts.append(doc.page_content)

#         # IMPORTANT
#         # Only primitive metadata goes into Chroma

#         metadatas.append({

#             "source": doc.metadata["source"],

#             "page": int(doc.metadata["page"]),

#             "chunk": int(doc.metadata["chunk"])

#         })

#         print(
#             f"Chunk {i} → "
#             f"{doc.metadata['source']} | "
#             f"Page {doc.metadata['page']} ✅"
#         )

#     print(f"\nTotal Vectors Created : {len(texts)}")

#     # ------------------------------------------
#     # Create Chroma
#     # ------------------------------------------

#     print("\n💾 Creating ChromaDB...")

#     vector_db = Chroma.from_texts(

#         texts=texts,

#         embedding=embedding_model,

#         metadatas=metadatas,

#         persist_directory="chroma_db"

#     )

#     print("✅ ChromaDB Created Successfully!")

#     # ------------------------------------------
#     # BM25
#     # ------------------------------------------

#     print("\n📚 Creating BM25 Index...")

#     tokenized_chunks = [

#         text.lower().split()

#         for text in texts

#     ]

#     bm25 = BM25Okapi(tokenized_chunks)

#     print("✅ BM25 Index Created Successfully!")

#     print("\n✅ Hybrid Search Ready!")

#     return vector_db, bm25

from langchain_chroma import Chroma
from rank_bm25 import BM25Okapi
import shutil
import os


def create_vector_store(documents, embedding_model):
    """
    Creates:

    1. ChromaDB (Semantic Search)
    2. BM25 Index

    ChromaDB only supports primitive metadata types,
    so we store only simple metadata there.
    """

    print("\n🔄 Converting Chunks into Embeddings...\n")

    texts = []

    metadatas = []

    # ------------------------------------------
    # Delete old ChromaDB
    # ------------------------------------------

    if os.path.exists("chroma_db"):

        shutil.rmtree("chroma_db")

        print("🗑 Old ChromaDB Deleted")

    # ------------------------------------------
    # Prepare Data
    # ------------------------------------------

    for i, doc in enumerate(documents, start=1):

        texts.append(doc.page_content)

        # IMPORTANT
        # Only primitive metadata goes into Chroma

        metadatas.append({

            "source": doc.metadata["source"],

            "page": int(doc.metadata["page"]),

            "chunk": int(doc.metadata["chunk"])

        })

        print(
            f"Chunk {i} → "
            f"{doc.metadata['source']} | "
            f"Page {doc.metadata['page']} ✅"
        )

    print(f"\nTotal Vectors Created : {len(texts)}")

    # ------------------------------------------
    # Create Chroma
    # ------------------------------------------

    print("\n💾 Creating ChromaDB...")

    vector_db = Chroma.from_texts(

        texts=texts,

        embedding=embedding_model,

        metadatas=metadatas,

        persist_directory="chroma_db"

    )

    print("✅ ChromaDB Created Successfully!")

    # ------------------------------------------
    # BM25
    # ------------------------------------------

    print("\n📚 Creating BM25 Index...")

    tokenized_chunks = [

        text.lower().split()

        for text in texts

    ]

    bm25 = BM25Okapi(tokenized_chunks)

    print("✅ BM25 Index Created Successfully!")

    print("\n✅ Hybrid Search Ready!")

    return vector_db, bm25


def load_existing_vector_store(embedding_model):
    """
    Reload a previously persisted ChromaDB WITHOUT deleting or
    rebuilding it. Returns None if no persisted store exists yet.

    Used by the process_pdf() cache-skip path so that restarting the
    backend doesn't force a full re-embed of every PDF when nothing
    has changed on disk.
    """

    if not os.path.exists("chroma_db"):
        return None

    vector_db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_model,
    )

    return vector_db