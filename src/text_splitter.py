# # # # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # # # from langchain_core.documents import Document


# # # # def split_text(pdf):
# # # #     """
# # # #     Split PDF into semantic chunks while preserving
# # # #     page metadata for images and tables.
# # # #     """

# # # #     splitter = RecursiveCharacterTextSplitter(

# # # #         chunk_size=1500,

# # # #         chunk_overlap=300,

# # # #         separators=[
# # # #             "\n\n",
# # # #             "\n",
# # # #             ". ",
# # # #             "? ",
# # # #             "! ",
# # # #             " ",
# # # #             ""
# # # #         ]
# # # #     )

# # # #     documents = []

# # # #     chunk_no = 1

# # # #     for page in pdf["content"]:

# # # #         page_number = page["page"]

# # # #         text = page["text"]
# # # #         tables = page.get("tables", [])

# # # #         images = page.get("images", [])

# # # #         figures = page.get("figures", [])

# # # #         page_image = page.get("page_image", "")

# # # #         if not text.strip():
# # # #             continue

# # # #         chunks = splitter.split_text(text)

# # # #         for chunk in chunks:

# # # #             doc = Document(

# # # #                 page_content=chunk,

# # # #                 metadata={

# # # #                   "source": pdf["file_name"],

# # # #                    "page": page_number,

# # # #                    "chunk": chunk_no,

# # # #                     "tables": tables,

# # # #                     "images": images,

# # # #                   "page_image": page_image

# # # #                 }

# # # #             )

# # # #             documents.append(doc)

# # # #             chunk_no += 1

# # # #     print(f"\n📄 {pdf['file_name']}")
# # # #     print(f"Pages   : {pdf['pages']}")
# # # #     print(f"Chunks  : {len(documents)}")

# # # #     return documents
# # # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # # from langchain_core.documents import Document


# # # def split_text(pdf):
# # #     """
# # #     Split PDF into:
# # #     - Text chunks
# # #     - Individual images
# # #     - Figures
# # #     - Tables metadata

# # #     Keeps page information in metadata.
# # #     """

# # #     splitter = RecursiveCharacterTextSplitter(

# # #         chunk_size=1500,

# # #         chunk_overlap=300,

# # #         separators=[
# # #             "\n\n",
# # #             "\n",
# # #             ". ",
# # #             "? ",
# # #             "! ",
# # #             " ",
# # #             ""
# # #         ]
# # #     )


# # #     documents = []

# # #     chunk_no = 1


# # #     for page in pdf["content"]:

# # #         page_number = page["page"]

# # #         text = page.get("text", "")

# # #         tables = page.get("tables", [])

# # #         images = page.get("images", [])

# # #         figures = page.get("figures", [])

# # #         page_image = page.get("page_image", "")



# # #         # ==================================
# # #         # TEXT CHUNK EXTRACTION
# # #         # ==================================

# # #         if text.strip():

# # #             chunks = splitter.split_text(text)


# # #             for chunk in chunks:


# # #                 doc = Document(

# # #                     page_content=chunk,


# # #                     metadata={

# # #                         "source": pdf["file_name"],

# # #                         "page": page_number,

# # #                         "chunk": chunk_no,

# # #                         "type": "text",

# # #                         "tables": tables,

# # #                         "page_image": page_image

# # #                     }

# # #                 )


# # #                 documents.append(doc)


# # #                 chunk_no += 1




# # #         # ==================================
# # #         # INDIVIDUAL IMAGE EXTRACTION
# # #         # ==================================

# # #         for img_no, image in enumerate(images):


# # #             image_doc = Document(


# # #                 page_content=f"Image from page {page_number}",


# # #                 metadata={


# # #                     "source": pdf["file_name"],

# # #                     "page": page_number,

# # #                     "chunk": chunk_no,

# # #                     "type": "image",

# # #                     "image_number": img_no + 1,

# # #                     "image_path": image


# # #                 }

# # #             )


# # #             documents.append(image_doc)



# # #             print("\n🖼️ IMAGE EXTRACTED")

# # #             print("----------------------")

# # #             print("PDF       :", pdf["file_name"])

# # #             print("Page      :", page_number)

# # #             print("Image No. :", img_no + 1)

# # #             print("Path      :", image)



# # #             chunk_no += 1





# # #         # ==================================
# # #         # FIGURE EXTRACTION
# # #         # ==================================

# # #         for fig_no, figure in enumerate(figures):


# # #             figure_doc = Document(


# # #                 page_content=f"Figure from page {page_number}",


# # #                 metadata={


# # #                     "source": pdf["file_name"],

# # #                     "page": page_number,

# # #                     "chunk": chunk_no,

# # #                     "type": "figure",

# # #                     "figure_number": fig_no + 1,

# # #                     "figure_path": figure


# # #                 }

# # #             )


# # #             documents.append(figure_doc)



# # #             print("\n📊 FIGURE EXTRACTED")

# # #             print("----------------------")

# # #             print("PDF        :", pdf["file_name"])

# # #             print("Page       :", page_number)

# # #             print("Figure No. :", fig_no + 1)

# # #             print("Path       :", figure)



# # #             chunk_no += 1





# # #     # ==================================
# # #     # FINAL SUMMARY
# # #     # ==================================

# # #     print("\n==============================")

# # #     print("📄 PDF NAME :", pdf["file_name"])

# # #     print("📑 TOTAL PAGES :", pdf["pages"])

# # #     print("📦 TOTAL DOCUMENTS :", len(documents))


# # #     text_count = len(
# # #         [
# # #             d for d in documents 
# # #             if d.metadata["type"] == "text"
# # #         ]
# # #     )


# # #     image_count = len(
# # #         [
# # #             d for d in documents
# # #             if d.metadata["type"] == "image"
# # #         ]
# # #     )


# # #     figure_count = len(
# # #         [
# # #             d for d in documents
# # #             if d.metadata["type"] == "figure"
# # #         ]
# # #     )


# # #     print("📝 Text Chunks :", text_count)

# # #     print("🖼️ Images      :", image_count)

# # #     print("📊 Figures     :", figure_count)


# # #     print("==============================")


# # #     return documents
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_core.documents import Document



# # def split_text(pdf):

# #     """
# #     Split PDF into:

# #     - Text chunks
# #     - Individual extracted images
# #     - Figures
# #     - Tables

# #     Keeps page metadata.
# #     """


# #     splitter = RecursiveCharacterTextSplitter(

# #         chunk_size=1500,

# #         chunk_overlap=300,

# #         separators=[
# #             "\n\n",
# #             "\n",
# #             ". ",
# #             "? ",
# #             "! ",
# #             " ",
# #             ""
# #         ]

# #     )


# #     documents = []

# #     chunk_no = 1



# #     for page in pdf["content"]:


# #         page_number = page["page"]


# #         # =====================================
# #         # GET TEXT FROM TEXT BLOCKS
# #         # =====================================

# #         text_blocks = page.get(
# #             "text_blocks",
# #             []
# #         )


# #         text = "\n".join(

# #             block["text"]

# #             for block in text_blocks

# #         )


# #         tables = page.get(
# #             "tables",
# #             []
# #         )


# #         images = page.get(
# #             "images",
# #             []
# #         )


# #         figures = page.get(
# #             "figures",
# #             []
# #         )


# #         page_image = page.get(
# #             "page_image",
# #             ""
# #         )



# #         # =====================================
# #         # TEXT CHUNKS
# #         # =====================================


# #         if text.strip():


# #             chunks = splitter.split_text(text)



# #             for chunk in chunks:


# #                 doc = Document(

# #                     page_content=chunk,


# #                     metadata={


# #                         "source": pdf["file_name"],

# #                         "page": page_number,

# #                         "chunk": chunk_no,

# #                         "type": "text",

# #                         "tables": tables,

# #                         "page_image": page_image

# #                     }

# #                 )


# #                 documents.append(doc)

# #                 chunk_no += 1





# #         # =====================================
# #         # ORIGINAL PDF IMAGES
# #         # =====================================


# #         for img_no, image in enumerate(images):


# #             image_doc = Document(


# #                 page_content=(

# #                     f"Image from page {page_number}. "

# #                     f"Machine Learning diagram or visual content."

# #                 ),


# #                 metadata={


# #                     "source": pdf["file_name"],

# #                     "page": page_number,

# #                     "chunk": chunk_no,

# #                     "type": "image",

# #                     "image_number": img_no + 1,

# #                     "image_path": image,

# #                     "page_image": page_image

# #                 }

# #             )


# #             documents.append(image_doc)



# #             print("\n🖼️ IMAGE EXTRACTED")

# #             print("----------------------")

# #             print(
# #                 "PDF       :",
# #                 pdf["file_name"]
# #             )

# #             print(
# #                 "Page      :",
# #                 page_number
# #             )

# #             print(
# #                 "Image No. :",
# #                 img_no + 1
# #             )

# #             print(
# #                 "Path      :",
# #                 image
# #             )



# #             chunk_no += 1





# #         # =====================================
# #         # FIGURES
# #         # =====================================


# #         for fig_no, figure in enumerate(figures):


# #             figure_doc = Document(


# #                 page_content=(

# #                     f"Figure from page {page_number}. "

# #                     "Contains diagram, chart or illustration."

# #                 ),


# #                 metadata={


# #                     "source": pdf["file_name"],

# #                     "page": page_number,

# #                     "chunk": chunk_no,

# #                     "type": "figure",

# #                     "figure_number": fig_no + 1,

# #                     "figure_path": figure["path"],

# #                     "bbox": figure["bbox"],

# #                     "page_image": page_image

# #                 }

# #             )


# #             documents.append(figure_doc)



# #             print("\n📊 FIGURE EXTRACTED")

# #             print("----------------------")

# #             print(
# #                 "PDF        :",
# #                 pdf["file_name"]
# #             )

# #             print(
# #                 "Page       :",
# #                 page_number
# #             )

# #             print(
# #                 "Figure No. :",
# #                 fig_no + 1
# #             )

# #             print(
# #                 "Path       :",
# #                 figure["path"]
# #             )



# #             chunk_no += 1






# #     # =====================================
# #     # SUMMARY
# #     # =====================================


# #     print("\n==============================")

# #     print(
# #         "📄 PDF NAME :",
# #         pdf["file_name"]
# #     )

# #     print(
# #         "📑 TOTAL PAGES :",
# #         pdf["pages"]
# #     )

# #     print(
# #         "📦 TOTAL DOCUMENTS :",
# #         len(documents)
# #     )


# #     print(
# #         "📝 Text Chunks :",
# #         len(
# #             [
# #                 d for d in documents
# #                 if d.metadata["type"]=="text"
# #             ]
# #         )
# #     )


# #     print(
# #         "🖼️ Images :",
# #         len(
# #             [
# #                 d for d in documents
# #                 if d.metadata["type"]=="image"
# #             ]
# #         )
# #     )


# #     print(
# #         "📊 Figures :",
# #         len(
# #             [
# #                 d for d in documents
# #                 if d.metadata["type"]=="figure"
# #             ]
# #         )
# #     )


# #     print("==============================")


# #     return documents
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document


# def split_text(pdf):
#     """
#     Split PDF into:
#     - Text chunks
#     - Individual images
#     - Figures

#     Keeps page metadata for retrieval.
#     """

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1500,
#         chunk_overlap=300,
#         separators=[
#             "\n\n",
#             "\n",
#             ". ",
#             "? ",
#             "! ",
#             " ",
#             ""
#         ]
#     )

#     documents = []
#     chunk_no = 1

#     for page in pdf["content"]:

#         page_number = page["page"]

#         # Support both loader formats
#         if "text" in page:
#             text = page.get("text", "")
#         else:
#             text_blocks = page.get("text_blocks", [])
#             text = "\n".join(
#                 block.get("text", "")
#                 for block in text_blocks
#             )

#         tables = page.get("tables", [])
#         images = page.get("images", [])
#         figures = page.get("figures", [])
#         page_image = page.get("page_image", "")

#         # =====================================
#         # TEXT CHUNKS
#         # =====================================

#         if text.strip():

#             chunks = splitter.split_text(text)

#             for chunk in chunks:

#                 documents.append(
#                     Document(
#                         page_content=chunk,
#                         metadata={
#                             "type": "text",
#                             "source": pdf["file_name"],
#                             "page": page_number,
#                             "chunk": chunk_no,
#                             "tables": tables,
#                             "page_image": page_image
#                         }
#                     )
#                 )

#                 chunk_no += 1

#         # =====================================
#         # IMAGE DOCUMENTS
#         # =====================================

#         for img_no, image_path in enumerate(images):

#             documents.append(
#                 Document(
#                     page_content=f"Image on page {page_number}",
#                     metadata={
#                         "type": "image",
#                         "source": pdf["file_name"],
#                         "page": page_number,
#                         "chunk": chunk_no,
#                         "image_number": img_no + 1,
#                         "image_path": image_path,
#                         "page_image": page_image
#                     }
#                 )
#             )

#             print("\n🖼️ IMAGE EXTRACTED")
#             print("----------------------")
#             print("PDF       :", pdf["file_name"])
#             print("Page      :", page_number)
#             print("Image No. :", img_no + 1)
#             print("Path      :", image_path)

#             chunk_no += 1

#         # =====================================
#         # FIGURE DOCUMENTS
#         # =====================================

#         for fig_no, figure in enumerate(figures):

#             documents.append(
#                 Document(
#                     page_content=f"Figure on page {page_number}",
#                     metadata={
#                         "type": "figure",
#                         "source": pdf["file_name"],
#                         "page": page_number,
#                         "chunk": chunk_no,
#                         "figure_number": fig_no + 1,
#                         "figure_path": figure["path"],
#                         "bbox": figure.get("bbox"),
#                         "ocr_text": figure.get("ocr_text", ""),
#                         "page_image": page_image
#                     }
#                 )
#             )

#             print("\n📊 FIGURE EXTRACTED")
#             print("----------------------")
#             print("PDF       :", pdf["file_name"])
#             print("Page      :", page_number)
#             print("Figure No.:", fig_no + 1)
#             print("Path      :", figure["path"])

#             chunk_no += 1

#     print("\n==============================")
#     print("PDF :", pdf["file_name"])
#     print("Documents :", len(documents))
#     print("==============================")

#     return documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_text(pdf):
    """
    Split PDF into

    1. Text Documents
    2. Image Documents
    3. Figure Documents
    4. Table Documents

    Each document keeps complete metadata so the
    retriever can retrieve the correct object.
    """

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1500,

        chunk_overlap=300,

        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            " ",
            ""
        ]

    )

    documents = []

    chunk_no = 1

    for page in pdf["content"]:

        page_number = page["page"]

        # ==========================================
        # PAGE DATA
        # ==========================================

        text = page.get("text", "")

        if not text:

            text_blocks = page.get("text_blocks", [])

            text = "\n".join(

                block.get("text", "")

                for block in text_blocks

            )

        images = page.get("images", [])

        figures = page.get("figures", [])

        tables = page.get("tables", [])

        raw_tables = page.get("raw_tables", [])

        page_image = page.get("page_image", "")

        # ==========================================
        # TEXT DOCUMENTS
        # ==========================================

        if text.strip():

            chunks = splitter.split_text(text)

            for chunk in chunks:

                documents.append(

                    Document(

                        page_content=chunk,

                        metadata={

                            "type": "text",

                            "source": pdf["file_name"],

                            "page": page_number,

                            "chunk": chunk_no,

                            "page_image": page_image,

                            "tables": tables,

                            "images": images,

                            "figures": figures

                        }

                    )

                )

                chunk_no += 1

        # ==========================================
        # IMAGE DOCUMENTS
        # ==========================================

        for img_no, image_path in enumerate(images):

            documents.append(

                Document(

                    page_content=f"Image from page {page_number}",

                    metadata={

                        "type": "image",

                        "source": pdf["file_name"],

                        "page": page_number,

                        "chunk": chunk_no,

                        "image_number": img_no + 1,

                        "image_path": image_path,

                        "page_image": page_image

                    }

                )

            )

            print("\n🖼 IMAGE DOCUMENT CREATED")
            print("PDF :", pdf["file_name"])
            print("Page:", page_number)
            print("Image:", img_no + 1)

            chunk_no += 1
                    # ==========================================
        # FIGURE DOCUMENTS
        # ==========================================

        for fig_no, figure in enumerate(figures):

            documents.append(

                Document(

                    page_content=(

                        figure.get(
                            "ocr_text",
                            f"Figure from page {page_number}"
                        )

                    ),

                    metadata={

                        "type": "figure",

                        "source": pdf["file_name"],

                        "page": page_number,

                        "chunk": chunk_no,

                        "figure_number": fig_no + 1,

                        "figure_path": figure.get("path"),

                        "bbox": figure.get("bbox"),

                        "ocr_text": figure.get("ocr_text", ""),

                        "page_image": page_image

                    }

                )

            )

            print("\n📊 FIGURE DOCUMENT CREATED")
            print("PDF :", pdf["file_name"])
            print("Page:", page_number)
            print("Figure:", fig_no + 1)

            chunk_no += 1

        # ==========================================
        # TABLE DOCUMENTS
        # ==========================================

        for table_no, table in enumerate(tables):

            table_text = ""

            if table_no < len(raw_tables):
                table_text = raw_tables[table_no]

            documents.append(

                Document(

                    page_content=table_text,

                    metadata={

                        "type": "table",

                        "source": pdf["file_name"],

                        "page": page_number,

                        "chunk": chunk_no,

                        "table_number": table_no + 1,

                        "table_path": table.get("path"),

                        "bbox": table.get("bbox"),

                        "ocr_text": table.get("ocr_text", ""),

                        "page_image": page_image

                    }

                )

            )

            print("\n📋 TABLE DOCUMENT CREATED")
            print("PDF :", pdf["file_name"])
            print("Page:", page_number)
            print("Table:", table_no + 1)

            chunk_no += 1

    # ==========================================
    # SUMMARY
    # ==========================================

    text_count = len(
        [d for d in documents if d.metadata["type"] == "text"]
    )

    image_count = len(
        [d for d in documents if d.metadata["type"] == "image"]
    )

    figure_count = len(
        [d for d in documents if d.metadata["type"] == "figure"]
    )

    table_count = len(
        [d for d in documents if d.metadata["type"] == "table"]
    )

    print("\n" + "=" * 60)
    print("TEXT SPLITTER SUMMARY")
    print("=" * 60)
    print("PDF           :", pdf["file_name"])
    print("Text Chunks   :", text_count)
    print("Images        :", image_count)
    print("Figures       :", figure_count)
    print("Tables        :", table_count)
    print("Total Docs    :", len(documents))
    print("=" * 60)

    return documents