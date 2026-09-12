# # # import os
# # # from PIL import Image

# # # from src.pdf_loader import load_all_pdfs
# # # from src.text_splitter import split_text
# # # from src.embeddings import get_embedding_model
# # # from src.vector_store import create_vector_store
# # # from src.retriever import retrieve_chunks
# # # from src.reranker import Reranker
# # # from src.llm import GroqLLM

# # # from src.pdf_router import PDFRouter
# # # from src.memory import ConversationMemory
# # # from src.tools import ToolManager
# # # from src.image_retriever import ImageRetriever
# # # from src.table_retriever import TableRetriever

# # # class RAGPipeline:

# # #     def __init__(self):
# # #         self.image_retriever = ImageRetriever()

# # #         self.table_retriever = TableRetriever()
# # #         print("=" * 70)
# # #         print("          ADVANCED MULTI PDF RAG CHATBOT")
# # #         print("=" * 70)

# # #         print("\n🧠 Loading Embedding Model...")
# # #         print("Model : BAAI/bge-small-en-v1.5")

# # #         self.embedding_model = get_embedding_model()

# # #         print("✅ Embedding Model Loaded Successfully!")

# # #         self.router = PDFRouter()

# # #         self.memory = ConversationMemory()

# # #         self.tool_manager = ToolManager()

# # #         self.llm = GroqLLM()

# # #         self.reranker = Reranker()

# # #         self.vector_db = None
# # #         self.bm25 = None
# # #         self.documents = None

# # #     # =======================================================
# # #     # PROCESS PDF
# # #     # =======================================================

# # #     def process_pdf(self, folder_path):

# # #         print("\n📂 Loading PDFs...")

# # #         pdfs = load_all_pdfs(folder_path)

# # #         print("\n✂ Splitting PDFs into Chunks...")

# # #         all_chunks = []

# # #         total_pages = 0

# # #         pdf_statistics = []

# # #         for pdf in pdfs:

# # #             total_pages += pdf["pages"]

# # #             chunks = split_text(pdf)

# # #             all_chunks.extend(chunks)

# # #             total_characters = sum(
# # #                 len(page["text"])
# # #                 for page in pdf["content"]
# # #             )

# # #             pdf_statistics.append({

# # #                 "file_name": pdf["file_name"],

# # #                 "pages": pdf["pages"],

# # #                 "characters": total_characters,

# # #                 "chunks": len(chunks),

# # #                 "images": pdf["total_images"],

# # #                 "tables": pdf["total_tables"]

# # #             })

# # #         print("\n✅ Chunking Completed!")

# # #         self.vector_db, self.bm25 = create_vector_store(

# # #             all_chunks,

# # #             self.embedding_model

# # #         )

# # #         self.documents = all_chunks

# # #         print("\n")
# # #         print("=" * 60)
# # #         print("        PDF PROCESSING SUMMARY")
# # #         print("=" * 60)

# # #         for i, stat in enumerate(pdf_statistics, start=1):

# # #             print(f"\nPDF {i}")
# # #             print("-" * 40)
# # #             print(f"File Name   : {stat['file_name']}")
# # #             print(f"Pages       : {stat['pages']}")
# # #             print(f"Characters  : {stat['characters']}")
# # #             print(f"Chunks      : {stat['chunks']}")
# # #             print(f"Images      : {stat['images']}")
# # #             print(f"Tables      : {stat['tables']}")

# # #         print("\n" + "=" * 60)
# # #         print("PDF PROCESSING COMPLETED")
# # #         print("=" * 60)
# # #         print(f"PDFs Loaded      : {len(pdfs)}")
# # #         print(f"Total Pages      : {total_pages}")
# # #         print(f"Total Chunks     : {len(all_chunks)}")
# # #         print("Embedding Model  : BAAI/bge-small-en-v1.5")
# # #         print("Retriever        : Hybrid Search (ChromaDB + BM25)")
# # #         print("Router           : PDF Router")
# # #         print("Reranker         : CrossEncoder")
# # #         print("Memory           : Conversation Memory")
# # #         print("LLM              : Groq")
# # #         print("=" * 60)

# # #     # =======================================================
# # #     # ASK
# # #     # =======================================================

# # #     def ask(self, query):

# # #         print("\n" + "=" * 60)
# # #         print("QUESTION")
# # #         print("=" * 60)
# # #         print(query)

# # #         tool = self.tool_manager.select_tool(query)

# # #         print(f"\n🔧 Selected Tool : {tool}")

# # #         # ===================================================
# # #         # MEMORY
# # #         # ===================================================

# # #         if tool == "memory":

# # #             history = self.memory.get_context()

# # #             print("\n========== MEMORY ==========")
# # #             print(history)

# # #             return history

# # #         # ===================================================
# # #         # ROUTE PDF
# # #         # ===================================================

# # #         selected_pdf = self.router.route(
# # #             self.vector_db,
# # #             query
# # #         )

# # #         print(f"\n📂 Routed PDF : {selected_pdf}")

# # #         retrieved = retrieve_chunks(

# # #             self.vector_db,

# # #             self.bm25,

# # #             self.documents,

# # #             query,

# # #             selected_pdf,

# # #             k=3

# # #         )

# # #         if len(retrieved) == 0:

# # #             print("\n❌ No matching content found.")

# # #             return

# # #         doc = retrieved[0]
# # #         print("\n========== METADATA ==========")
# # #         print(f"Source PDF : {doc.metadata.get('source')}")
# # #         print(f"Page       : {doc.metadata.get('page')}")
# # #         print(f"Chunk      : {doc.metadata.get('chunk')}")
# # #         print(f"Page Image : {doc.metadata.get('page_image')}")

# # #         tables = doc.metadata.get("tables", [])
# # #         figures = doc.metadata.get("figures", [])

# # #         print(f"Tables Found : {len(tables)}")
# # #         print(f"Figures Found : {len(figures)}")

# # #         for fig in figures:
# # #          print("Figure :", fig)
# # #         print("==============================")
# # # # IMAGE TOOL
# # # # ===================================================

# # #         if tool == "image":

# # #           print("\n🖼 IMAGE TOOL")

# # #           self.image_retriever.show_image(doc)

# # #           return
# # #         # if tool == "image":

# # #         #     print("\n🖼 IMAGE TOOL")

# # #         #     page_image = doc.metadata.get("page_image", "")

# # #         #     print(f"\n📄 PDF  : {doc.metadata['source']}")
# # #         #     print(f"📄 Page : {doc.metadata['page']}")

# # #         #     if page_image and os.path.exists(page_image):

# # #         #         print(f"\nOpening page image...\n{page_image}")

# # #         #         try:

# # #         #             img = Image.open(page_image)

# # #         #             img.show()

# # #         #         except Exception as e:

# # #         #             print(f"Unable to open image: {e}")

# # #         #     else:

# # #         #         print("\n❌ Page image not found.")

# # #         #     return

# # #         # ===================================================
# # #         # TABLE TOOL
# # #         # ===================================================

# # #         # if tool == "table":
# # #           # ===================================================
# # # # TABLE TOOL
# # # # ===================================================

# # #         if tool == "table":

# # #           print("\n📊 TABLE TOOL")

# # #           self.table_retriever.show_tables(doc)

# # #           return
# # #         #     print("\n📊 TABLE TOOL")

# # #         #     tables = doc.metadata.get("tables", [])

# # #         #     print(f"\n📄 PDF  : {doc.metadata['source']}")
# # #         #     print(f"📄 Page : {doc.metadata['page']}")

# # #         #     if len(tables) == 0:

# # #         #         print("\n❌ No table detected on this page.")

# # #         #     else:

# # #         #         print("\n========== TABLES ==========\n")

# # #         #         for i, table in enumerate(tables, start=1):

# # #         #             print(f"Table {i}")

# # #         #             print("-" * 60)

# # #         #             print(table)

# # #         #             print("-" * 60)

# # #         #     page_image = doc.metadata.get("page_image", "")

# # #         #     if page_image and os.path.exists(page_image):

# # #         #         print("\nOpening page containing the table...")

# # #         #         try:

# # #         #             img = Image.open(page_image)

# # #         #             img.show()

# # #         #         except Exception as e:

# # #         #             print(e)

# # #         #     return

# # #         # ===================================================
# # #         # NORMAL RAG
# # #         # ===================================================

# # #         final_chunks = self.reranker.rerank(

# # #             query,

# # #             retrieved

# # #         )

# # #         print("\n========== FINAL RETRIEVED CHUNKS ==========")

# # #         context = ""

# # #         for i, doc in enumerate(final_chunks, start=1):

# # #             print(f"\nRank {i}")

# # #             print(f"Source : {doc.metadata['source']}")

# # #             print(f"Page   : {doc.metadata['page']}")

# # #             print("-" * 50)

# # #             print(doc.page_content[:350])

# # #             print("-" * 50)

# # #             context += doc.page_content + "\n\n"

# # #         memory_context = self.memory.get_context()

# # #         print("\n🤖 Sending Context to Groq...\n")

# # #         answer = self.llm.generate_answer(

# # #             context=context,

# # #             question=query,

# # #             memory=memory_context

# # #         )

# # #         self.memory.add(

# # #             query,

# # #             answer

# # #         )

# # #         print("\n" + "=" * 60)

# # #         print("FINAL ANSWER")

# # #         print("=" * 60)

# # #         print(answer)

# # #         print("=" * 60)

# # #         return answer
# # import os
# # from PIL import Image

# # from src.pdf_loader import load_all_pdfs
# # from src.text_splitter import split_text
# # from src.embeddings import get_embedding_model
# # from src.vector_store import create_vector_store
# # from src.retriever import retrieve_chunks
# # from src.reranker import Reranker
# # from src.llm import GroqLLM

# # from src.pdf_router import PDFRouter
# # from src.memory import ConversationMemory
# # from src.tools import ToolManager
# # from src.image_retriever import ImageRetriever
# # from src.table_retriever import TableRetriever


# # class RAGPipeline:


# #     def __init__(self):

# #         self.image_retriever = ImageRetriever()

# #         self.table_retriever = TableRetriever()


# #         print("=" * 70)
# #         print("          ADVANCED MULTI PDF RAG CHATBOT")
# #         print("=" * 70)



# #         print("\n🧠 Loading Embedding Model...")
# #         print("Model : BAAI/bge-small-en-v1.5")


# #         self.embedding_model = get_embedding_model()


# #         print("✅ Embedding Model Loaded Successfully!")


# #         self.router = PDFRouter()

# #         self.memory = ConversationMemory()

# #         self.tool_manager = ToolManager()


# #         self.llm = GroqLLM()

# #         self.reranker = Reranker()


# #         self.vector_db = None

# #         self.bm25 = None

# #         self.documents = None




# #     # =======================================================
# #     # PROCESS PDF
# #     # =======================================================


# #     def process_pdf(self, folder_path):


# #         print("\n📂 Loading PDFs...")


# #         pdfs = load_all_pdfs(folder_path)



# #         print("\n✂ Splitting PDFs into Chunks...")


# #         all_chunks = []

# #         total_pages = 0

# #         pdf_statistics = []



# #         for pdf in pdfs:


# #             total_pages += pdf["pages"]



# #             chunks = split_text(pdf)



# #             all_chunks.extend(chunks)



# #             # ==========================================
# #             # CHARACTER COUNT FIX
# #             # ==========================================


# #             total_characters = sum(

# #                 len(

# #                     "\n".join(

# #                         block["text"]

# #                         for block in page.get(
# #                             "text_blocks",
# #                             []
# #                         )

# #                     )

# #                 )

# #                 for page in pdf["content"]

# #             )



# #             pdf_statistics.append({


# #                 "file_name": pdf["file_name"],

# #                 "pages": pdf["pages"],

# #                 "characters": total_characters,

# #                 "chunks": len(chunks),

# #                 "images": pdf["total_images"],

# #                 "tables": pdf["total_tables"]

# #             })




# #         print("\n✅ Chunking Completed!")



# #         self.vector_db, self.bm25 = create_vector_store(

# #             all_chunks,

# #             self.embedding_model

# #         )


# #         self.documents = all_chunks




# #         print("\n")

# #         print("=" * 60)

# #         print("        PDF PROCESSING SUMMARY")

# #         print("=" * 60)




# #         for i, stat in enumerate(
# #             pdf_statistics,
# #             start=1
# #         ):


# #             print(f"\nPDF {i}")

# #             print("-" * 40)

# #             print(
# #                 f"File Name   : {stat['file_name']}"
# #             )

# #             print(
# #                 f"Pages       : {stat['pages']}"
# #             )

# #             print(
# #                 f"Characters  : {stat['characters']}"
# #             )

# #             print(
# #                 f"Chunks      : {stat['chunks']}"
# #             )

# #             print(
# #                 f"Images      : {stat['images']}"
# #             )

# #             print(
# #                 f"Tables      : {stat['tables']}"
# #             )




# #         print("\n" + "=" * 60)

# #         print("PDF PROCESSING COMPLETED")

# #         print("=" * 60)


# #         print(
# #             f"PDFs Loaded      : {len(pdfs)}"
# #         )

# #         print(
# #             f"Total Pages      : {total_pages}"
# #         )

# #         print(
# #             f"Total Chunks     : {len(all_chunks)}"
# #         )

# #         print(
# #             "Embedding Model  : BAAI/bge-small-en-v1.5"
# #         )

# #         print(
# #             "Retriever        : Hybrid Search (ChromaDB + BM25)"
# #         )

# #         print(
# #             "Router           : PDF Router"
# #         )

# #         print(
# #             "Reranker         : CrossEncoder"
# #         )

# #         print(
# #             "Memory           : Conversation Memory"
# #         )

# #         print(
# #             "LLM              : Groq"
# #         )

# #         print("=" * 60)





# #     # =======================================================
# #     # ASK
# #     # =======================================================


# #     def ask(self, query):


# #         print("\n" + "=" * 60)

# #         print("QUESTION")

# #         print("=" * 60)

# #         print(query)




# #         tool = self.tool_manager.select_tool(query)


# #         print(
# #             f"\n🔧 Selected Tool : {tool}"
# #         )



# #         if tool == "memory":


# #             history = self.memory.get_context()


# #             print("\n========== MEMORY ==========")

# #             print(history)


# #             return history




# #         selected_pdf = self.router.route(

# #             self.vector_db,

# #             query

# #         )



# #         print(
# #             f"\n📂 Routed PDF : {selected_pdf}"
# #         )



# #         retrieved = retrieve_chunks(

# #             self.vector_db,

# #             self.bm25,

# #             self.documents,

# #             query,

# #             selected_pdf,

# #             k=3

# #         )



# #         if len(retrieved) == 0:


# #             print(
# #                 "\n❌ No matching content found."
# #             )

# #             return




# #         doc = retrieved[0]



# #         print("\n========== METADATA ==========")

# #         print(
# #             f"Source PDF : {doc.metadata.get('source')}"
# #         )

# #         print(
# #             f"Page       : {doc.metadata.get('page')}"
# #         )

# #         print(
# #             f"Chunk      : {doc.metadata.get('chunk')}"
# #         )

# #         print(
# #             f"Page Image : {doc.metadata.get('page_image')}"
# #         )



# #         print("==============================")




# #         # IMAGE TOOL

# #         if tool == "image":


# #             print("\n🖼 IMAGE TOOL")


# #             self.image_retriever.show_image(doc)


# #             return





# #         # TABLE TOOL


# #         # ===================================================
# # # TABLE TOOL
# # # ===================================================

# #         if tool == "table":

# #           print("\n📊 TABLE TOOL")

# #     # Keep only table documents
# #           table_docs = []

# #           for d in retrieved:

# #             if d.metadata.get("type") == "table":
# #               table_docs.append(d)

# #     # If no table found after retrieval
# #           if len(table_docs) == 0:

# #             print("\n❌ No table found for this query.")
     
# #             return

# #     # Rerank only table documents
# #           final_tables = self.reranker.rerank(
# #              query,
# #              table_docs
# #             )

# #           best_table = final_tables[0]
 
# #           print("\n========== SELECTED TABLE ==========")
# #           print("PDF   :", best_table.metadata["source"])
# #           print("Page  :", best_table.metadata["page"])
# #           print("Table :", best_table.metadata.get("table_number"))
# #           print("====================================")

# #           self.table_retriever.show_tables(best_table)

# #           return





# #         final_chunks = self.reranker.rerank(

# #             query,

# #             retrieved

# #         )



# #         print(
# #             "\n========== FINAL RETRIEVED CHUNKS =========="
# #         )



# #         context = ""



# #         for i, doc in enumerate(
# #             final_chunks,
# #             start=1
# #         ):


# #             print(
# #                 f"\nRank {i}"
# #             )


# #             print(
# #                 f"Source : {doc.metadata['source']}"
# #             )


# #             print(
# #                 f"Page   : {doc.metadata['page']}"
# #             )


# #             print("-" * 50)


# #             print(
# #                 doc.page_content[:350]
# #             )


# #             print("-" * 50)



# #             context += (
# #                 doc.page_content
# #                 +
# #                 "\n\n"
# #             )




# #         memory_context = self.memory.get_context()



# #         print(
# #             "\n🤖 Sending Context to Groq...\n"
# #         )



# #         answer = self.llm.generate_answer(

# #             context=context,

# #             question=query,

# #             memory=memory_context

# #         )



# #         self.memory.add(

# #             query,

# #             answer

# #         )



# #         print("\n" + "=" * 60)

# #         print("FINAL ANSWER")

# #         print("=" * 60)


# #         print(answer)


# #         print("=" * 60)



# #         return answer



# from PIL import Image

# from src.pdf_loader import load_all_pdfs
# from src.text_splitter import split_text
# from src.embeddings import get_embedding_model
# from src.vector_store import create_vector_store
# from src.retriever import retrieve_chunks
# from src.reranker import Reranker
# from src.llm import GroqLLM

# from src.pdf_router import PDFRouter
# from src.memory import ConversationMemory
# from src.tools import ToolManager
# from src.image_retriever import ImageRetriever
# from src.table_retriever import TableRetriever


# class RAGPipeline:

#     def __init__(self):

#         print("=" * 70)
#         print("          ADVANCED MULTI PDF RAG CHATBOT")
#         print("=" * 70)

#         self.image_retriever = ImageRetriever()
#         self.table_retriever = TableRetriever()

#         print("\n🧠 Loading Embedding Model...")
#         print("Model : BAAI/bge-small-en-v1.5")

#         self.embedding_model = get_embedding_model()

#         print("✅ Embedding Model Loaded Successfully!")

#         self.router = PDFRouter()
#         self.memory = ConversationMemory()
#         self.tool_manager = ToolManager()

#         self.llm = GroqLLM()
#         self.reranker = Reranker()

#         self.vector_db = None
#         self.bm25 = None
#         self.documents = None

#     # ==========================================================
#     # PROCESS PDF
#     # ==========================================================

#     def process_pdf(self, folder_path):

#         print("\n📂 Loading PDFs...")

#         pdfs = load_all_pdfs(folder_path)

#         print("\n✂ Splitting PDFs into Chunks...")

#         all_chunks = []
#         total_pages = 0
#         pdf_statistics = []

#         for pdf in pdfs:

#             total_pages += pdf["pages"]

#             chunks = split_text(pdf)

#             all_chunks.extend(chunks)

#             total_characters = sum(
#                 len(page.get("text", ""))
#                 for page in pdf["content"]
#             )

#             pdf_statistics.append({

#                 "file_name": pdf["file_name"],
#                 "pages": pdf["pages"],
#                 "characters": total_characters,
#                 "chunks": len(chunks),
#                 "images": pdf["total_images"],
#                 "tables": pdf["total_tables"]

#             })

#         print("\n✅ Chunking Completed!")

#         self.vector_db, self.bm25 = create_vector_store(
#             all_chunks,
#             self.embedding_model
#         )

#         self.documents = all_chunks

#         print("\n")
#         print("=" * 60)
#         print("        PDF PROCESSING SUMMARY")
#         print("=" * 60)

#         for i, stat in enumerate(pdf_statistics, start=1):

#             print(f"\nPDF {i}")
#             print("-" * 40)
#             print(f"File Name   : {stat['file_name']}")
#             print(f"Pages       : {stat['pages']}")
#             print(f"Characters  : {stat['characters']}")
#             print(f"Chunks      : {stat['chunks']}")
#             print(f"Images      : {stat['images']}")
#             print(f"Tables      : {stat['tables']}")

#         print("\n" + "=" * 60)
#         print("PDF PROCESSING COMPLETED")
#         print("=" * 60)

#         print(f"PDFs Loaded      : {len(pdfs)}")
#         print(f"Total Pages      : {total_pages}")
#         print(f"Total Chunks     : {len(all_chunks)}")
#         print("Embedding Model  : BAAI/bge-small-en-v1.5")
#         print("Retriever        : Hybrid (Chroma + BM25)")
#         print("Reranker         : CrossEncoder")
#         print("LLM              : Groq")
#         print("=" * 60)

#     def ask(self, query):

#         print("\n" + "=" * 60)
#         print("QUESTION")
#         print("=" * 60)
#         print(query)

#         tool = self.tool_manager.select_tool(query)

#         print(f"\n🔧 Selected Tool : {tool}")

#         # =====================================================
#         # MEMORY
#         # =====================================================

#         if tool == "memory":

#             history = self.memory.get_context()

#             print("\n========== MEMORY ==========")
#             print(history)

#             return history

#         # =====================================================
#         # ROUTE PDF
#         # =====================================================

#         selected_pdf = self.router.route(
#             self.vector_db,
#             query
#         )

#         print(f"\n📂 Routed PDF : {selected_pdf}")

#         # =====================================================
#         # RETRIEVE
#         # =====================================================

#         retrieved = retrieve_chunks(
#             self.vector_db,
#             self.bm25,
#             self.documents,
#             query,
#             selected_pdf,
#             k=6
#         )

#         if len(retrieved) == 0:

#             print("\n❌ No matching content found.")
#             return

#         print("\n========== RETRIEVED DOCUMENTS ==========")

#         for d in retrieved:

#             print(
#                 f"{d.metadata.get('type','text')} | "
#                 f"Page {d.metadata.get('page')} | "
#                 f"{d.metadata.get('source')}"
#             )

#         # =====================================================
#         # IMAGE QUESTION
#         # =====================================================

#         if tool == "image":

#             print("\n🖼 IMAGE TOOL")

#             figure_docs = []

#             for d in retrieved:

#                 if d.metadata.get("type") == "figure":
#                     figure_docs.append(d)

#             if len(figure_docs) == 0:

#                 print("\n❌ No relevant figure found.")
#                 return

#             best_figure = self.reranker.rerank(
#                 query,
#                 figure_docs
#             )[0]

#             print("\n========== SELECTED FIGURE ==========")

#             print("PDF  :", best_figure.metadata["source"])
#             print("Page :", best_figure.metadata["page"])

#             self.image_retriever.show_image(best_figure)

#             return

#         # =====================================================
#         # TABLE QUESTION
#         # =====================================================

#         if tool == "table":

#             print("\n📊 TABLE TOOL")

#             table_docs = []

#             for d in retrieved:

#                 if d.metadata.get("type") == "table":
#                     table_docs.append(d)

#             if len(table_docs) == 0:

#                 print("\n❌ No table found.")
#                 return

#             best_table = self.reranker.rerank(
#                 query,
#                 table_docs
#             )[0]

#             print("\n========== SELECTED TABLE ==========")

#             print("PDF  :", best_table.metadata["source"])
#             print("Page :", best_table.metadata["page"])

#             self.table_retriever.show_tables(best_table)

#             return

#         # =====================================================
#         # THEORY QUESTION
#         # =====================================================

#         text_docs = []

#         for d in retrieved:

#             if d.metadata.get("type", "text") == "text":

#                 text_docs.append(d)

#         # Fallback if metadata wasn't set

#         if len(text_docs) == 0:

#             text_docs = retrieved

#         # -------------------------------

#         # Rerank ONLY text chunks

#         # -------------------------------

#         final_chunks = self.reranker.rerank(
#             query,
#             text_docs
#         )

#         print("\n========== FINAL RETRIEVED CHUNKS ==========")

#         context = ""

#         for i, doc in enumerate(final_chunks, start=1):

#             print(f"\nRank {i}")

#             print(f"Source : {doc.metadata.get('source')}")

#             print(f"Page   : {doc.metadata.get('page')}")

#             print(f"Chunk  : {doc.metadata.get('chunk')}")

#             print("-" * 60)

#             print(doc.page_content[:500])

#             print("-" * 60)

#             # Never send figures/tables to LLM

#             if doc.metadata.get("type") != "text":

#                 continue

#             context += doc.page_content

#             context += "\n\n"

#             if context.strip() == "":

#                 print("\n❌ No textual context found.")
#                 return

#         memory_context = self.memory.get_context()

#         print("\n🤖 Sending Context to Groq...\n")

#         answer = self.llm.generate_answer(
#             context=context,
#             question=query,
#             memory=memory_context
#         )

#         self.memory.add(
#             query,
#             answer
#         )

#         print("\n" + "=" * 60)

#         print("FINAL ANSWER")

#         print("=" * 60)

#         print(answer)

#         print("=" * 60)

#         return answer

import json
import os
import pickle

from PIL import Image

from rank_bm25 import BM25Okapi

from src.pdf_loader import load_all_pdfs
from src.text_splitter import split_text
from src.embeddings import get_embedding_model
from src.vector_store import create_vector_store, load_existing_vector_store
from src.retriever import retrieve_chunks
from src.reranker import Reranker
from src.llm import GroqLLM

from src.pdf_router import PDFRouter
from src.memory import ConversationMemory
from src.tools import ToolManager
from src.image_retriever import ImageRetriever
from src.table_retriever import TableRetriever


# ==============================================================
# PROCESSING CACHE
#
# ChromaDB only stores primitive metadata (source/page/chunk), so
# reloading Chroma alone is not enough to restore the richer chunk
# objects (type, page_image, figures, tables) that the rest of the
# pipeline depends on. So we separately cache the full processed
# chunk list, keyed to a fingerprint of the PDFs on disk. If the
# PDFs haven't changed since the last successful run, we skip
# PDF loading, OCR, YOLO and chunking entirely.
# ==============================================================

CACHE_MANIFEST_PATH = "chroma_db_manifest.json"
CACHE_CHUNKS_PATH = "processed_chunks.pkl"


def _build_pdf_manifest(folder_path):
    """Fingerprint of the PDFs in the data folder: name + size + mtime.

    If any PDF is added, removed, or modified, this fingerprint
    changes and a full reprocess is triggered automatically.
    """

    manifest = {}

    for fname in sorted(os.listdir(folder_path)):

        if fname.lower().endswith(".pdf"):

            full_path = os.path.join(folder_path, fname)
            stat = os.stat(full_path)

            manifest[fname] = {
                "size": stat.st_size,
                "mtime": stat.st_mtime,
            }

    return manifest


class RAGPipeline:

    def __init__(self):

        print("=" * 70)
        print("          ADVANCED MULTI PDF RAG CHATBOT")
        print("=" * 70)

        self.image_retriever = ImageRetriever()
        self.table_retriever = TableRetriever()

        print("\n🧠 Loading Embedding Model...")
        print("Model : BAAI/bge-small-en-v1.5")

        self.embedding_model = get_embedding_model()

        print("✅ Embedding Model Loaded Successfully!")

        self.router = PDFRouter()
        self.memory = ConversationMemory()
        self.tool_manager = ToolManager()

        self.llm = GroqLLM()
        self.reranker = Reranker()

        self.vector_db = None
        self.bm25 = None
        self.documents = None

    # ==========================================================
    # CACHE HELPERS
    # ==========================================================

    def _try_load_cached_index(self, current_manifest):
        """Attempt to reuse a previously processed index.

        Returns True and sets self.vector_db / self.bm25 / self.documents
        if a valid, matching cache was found and loaded. Returns False
        (and leaves everything untouched) if a full reprocess is needed.
        """

        if not os.path.exists(CACHE_MANIFEST_PATH):
            return False

        if not os.path.exists(CACHE_CHUNKS_PATH):
            return False

        if not os.path.exists("chroma_db"):
            return False

        try:
            with open(CACHE_MANIFEST_PATH, "r") as f:
                saved_manifest = json.load(f)
        except Exception:
            return False

        if saved_manifest != current_manifest:
            print(
                "\n♻️  PDFs in data folder have changed since last run "
                "— reprocessing required."
            )
            return False

        print(
            "\n⚡ Found existing processed index matching current PDFs "
            "— skipping PDF loading / OCR / YOLO / chunking."
        )

        try:
            with open(CACHE_CHUNKS_PATH, "rb") as f:
                all_chunks = pickle.load(f)

            vector_db = load_existing_vector_store(self.embedding_model)

            if vector_db is None:
                print("\n⚠️  chroma_db missing despite manifest — reprocessing.")
                return False

            print("\n📚 Rebuilding BM25 index from cached chunks...")

            tokenized_chunks = [
                c.page_content.lower().split()
                for c in all_chunks
            ]

            bm25 = BM25Okapi(tokenized_chunks)

            self.vector_db = vector_db
            self.bm25 = bm25
            self.documents = all_chunks

            print(
                f"✅ Loaded {len(all_chunks)} cached chunks. "
                "Vector DB and BM25 ready — no reprocessing needed!"
            )

            return True

        except Exception as exc:

            print(f"\n⚠️  Failed to load cached index ({exc}). Reprocessing PDFs.")
            return False

    def _save_cache(self, manifest, all_chunks):
        """Persist processed chunks + PDF fingerprint for fast future startups."""

        try:
            with open(CACHE_CHUNKS_PATH, "wb") as f:
                pickle.dump(all_chunks, f)

            with open(CACHE_MANIFEST_PATH, "w") as f:
                json.dump(manifest, f)

            print("\n💾 Saved processed chunks cache for faster future startups.")

        except Exception as exc:

            print(f"\n⚠️  Could not save processing cache: {exc}")

    # ==========================================================
    # PROCESS PDF
    # ==========================================================

    def process_pdf(self, folder_path):

        current_manifest = _build_pdf_manifest(folder_path)

        if self._try_load_cached_index(current_manifest):
            return

        print("\n📂 Loading PDFs...")

        pdfs = load_all_pdfs(folder_path)

        print("\n✂ Splitting PDFs into Chunks...")

        all_chunks = []
        total_pages = 0
        pdf_statistics = []

        for pdf in pdfs:

            total_pages += pdf["pages"]

            chunks = split_text(pdf)

            all_chunks.extend(chunks)

            total_characters = sum(
                len(page.get("text", ""))
                for page in pdf["content"]
            )

            pdf_statistics.append({

                "file_name": pdf["file_name"],
                "pages": pdf["pages"],
                "characters": total_characters,
                "chunks": len(chunks),
                "images": pdf["total_images"],
                "tables": pdf["total_tables"]

            })

        print("\n✅ Chunking Completed!")

        self.vector_db, self.bm25 = create_vector_store(
            all_chunks,
            self.embedding_model
        )

        self.documents = all_chunks

        # Persist the full chunk objects + PDF fingerprint so the next
        # startup can skip PDF loading / OCR / YOLO / chunking entirely,
        # as long as the PDFs in the data folder haven't changed.
        self._save_cache(current_manifest, all_chunks)

        print("\n")
        print("=" * 60)
        print("        PDF PROCESSING SUMMARY")
        print("=" * 60)

        for i, stat in enumerate(pdf_statistics, start=1):

            print(f"\nPDF {i}")
            print("-" * 40)
            print(f"File Name   : {stat['file_name']}")
            print(f"Pages       : {stat['pages']}")
            print(f"Characters  : {stat['characters']}")
            print(f"Chunks      : {stat['chunks']}")
            print(f"Images      : {stat['images']}")
            print(f"Tables      : {stat['tables']}")

        print("\n" + "=" * 60)
        print("PDF PROCESSING COMPLETED")
        print("=" * 60)

        print(f"PDFs Loaded      : {len(pdfs)}")
        print(f"Total Pages      : {total_pages}")
        print(f"Total Chunks     : {len(all_chunks)}")
        print("Embedding Model  : BAAI/bge-small-en-v1.5")
        print("Retriever        : Hybrid (Chroma + BM25)")
        print("Reranker         : CrossEncoder")
        print("LLM              : Groq")
        print("=" * 60)

    def ask(self, query):

        print("\n" + "=" * 60)
        print("QUESTION")
        print("=" * 60)
        print(query)

        tool = self.tool_manager.select_tool(query)

        print(f"\n🔧 Selected Tool : {tool}")

        # =====================================================
        # MEMORY
        # =====================================================

        if tool == "memory":

            history = self.memory.get_context()

            print("\n========== MEMORY ==========")
            print(history)

            return history

        # =====================================================
        # ROUTE PDF
        # =====================================================

        selected_pdf = self.router.route(
            self.vector_db,
            query
        )

        print(f"\n📂 Routed PDF : {selected_pdf}")

        # =====================================================
        # RETRIEVE
        # =====================================================

        retrieved = retrieve_chunks(
            self.vector_db,
            self.bm25,
            self.documents,
            query,
            selected_pdf,
            k=6
        )

        if len(retrieved) == 0:

            print("\n❌ No matching content found.")
            return "I couldn't find this information in the uploaded PDF."

        print("\n========== RETRIEVED DOCUMENTS ==========")

        for d in retrieved:

            print(
                f"{d.metadata.get('type','text')} | "
                f"Page {d.metadata.get('page')} | "
                f"{d.metadata.get('source')}"
            )

        # =====================================================
        # IMAGE QUESTION
        # =====================================================

        if tool == "image":

            print("\n🖼 IMAGE TOOL")

            figure_docs = []

            for d in retrieved:

                if d.metadata.get("type") == "figure":
                    figure_docs.append(d)

            if len(figure_docs) == 0:

                print("\n❌ No relevant figure found.")
                return

            best_figure = self.reranker.rerank(
                query,
                figure_docs
            )[0]

            print("\n========== SELECTED FIGURE ==========")

            print("PDF  :", best_figure.metadata["source"])
            print("Page :", best_figure.metadata["page"])

            self.image_retriever.show_image(best_figure)

            return

        # =====================================================
        # TABLE QUESTION
        # =====================================================

        if tool == "table":

            print("\n📊 TABLE TOOL")

            table_docs = []

            for d in retrieved:

                if d.metadata.get("type") == "table":
                    table_docs.append(d)

            if len(table_docs) == 0:

                print("\n❌ No table found.")
                return

            best_table = self.reranker.rerank(
                query,
                table_docs
            )[0]

            print("\n========== SELECTED TABLE ==========")

            print("PDF  :", best_table.metadata["source"])
            print("Page :", best_table.metadata["page"])

            self.table_retriever.show_tables(best_table)

            return

        # =====================================================
        # THEORY QUESTION
        # =====================================================

        text_docs = []

        for d in retrieved:

            if d.metadata.get("type", "text") == "text":

                text_docs.append(d)

        # Fallback: no pure "text" chunks matched, but we may still
        # have relevant table/figure chunks whose page_content is
        # readable prose (e.g. comparison tables extracted as text).
        # Use them as context instead of discarding everything and
        # falsely reporting no answer was found.
        used_fallback = False

        if len(text_docs) == 0:

            text_docs = retrieved
            used_fallback = True

        # -------------------------------

        # Rerank the candidate chunks

        # -------------------------------

        final_chunks = self.reranker.rerank(
            query,
            text_docs
        )

        print("\n========== FINAL RETRIEVED CHUNKS ==========")

        context = ""

        for i, doc in enumerate(final_chunks, start=1):

            print(f"\nRank {i}")

            print(f"Source : {doc.metadata.get('source')}")

            print(f"Page   : {doc.metadata.get('page')}")

            print(f"Chunk  : {doc.metadata.get('chunk')}")

            print("-" * 60)

            print(doc.page_content[:500])

            print("-" * 60)

            # Only exclude non-text chunks (figures/tables) when real
            # text chunks were actually found above. If we fell back
            # to table/figure chunks because nothing else matched,
            # use their content instead of silently sending nothing
            # to the LLM.
            if doc.metadata.get("type") != "text" and not used_fallback:

                continue

            context += doc.page_content

            context += "\n\n"

        if context.strip() == "":

            print("\n❌ No textual context found.")
            return "I couldn't find this information in the uploaded PDF."

        memory_context = self.memory.get_context()

        print("\n🤖 Sending Context to Groq...\n")

        answer = self.llm.generate_answer(
            context=context,
            question=query,
            memory=memory_context
        )

        self.memory.add(
            query,
            answer
        )

        print("\n" + "=" * 60)

        print("FINAL ANSWER")

        print("=" * 60)

        print(answer)

        print("=" * 60)

        return answer