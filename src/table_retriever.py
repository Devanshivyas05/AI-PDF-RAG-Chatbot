# import os
# from PIL import Image


# class TableRetriever:    

#     def __init__(self):
#         pass

#     def show_tables(self, document):
#         print("\n===== DEBUG =====")
#         print(document.metadata)
#         print("=================")
#         tables = document.metadata.get("tables", [])

#         print("\n" + "=" * 60)
#         print("TABLE RETRIEVER")
#         print("=" * 60)

#         print(f"PDF  : {document.metadata['source']}")
#         print(f"Page : {document.metadata['page']}")

#         if len(tables) == 0:

#             print("\n❌ No table detected.")

#         else:

#             print("\n========== TABLES ==========\n")

#             for i, table in enumerate(tables, start=1):

#                 print(f"Table {i}")
#                 print("-" * 60)
#                 print(table)
#                 print("-" * 60)

#         page_image = document.metadata.get("page_image", "")

#         if page_image and os.path.exists(page_image):

#             print("\nOpening page containing the table...")

#             image = Image.open(page_image)

#             image.show()
import os
from PIL import Image


class TableRetriever:

    def __init__(self):
        pass

    def show_tables(self, document):

        print("\n" + "=" * 60)
        print("TABLE RETRIEVER")
        print("=" * 60)

        print(f"PDF  : {document.metadata.get('source')}")
        print(f"Page : {document.metadata.get('page')}")

        table_path = None

        # ==========================================
        # Cropped Table (Highest Priority)
        # ==========================================

        if document.metadata.get("type") == "table":

            table_path = document.metadata.get("table_path")

            print("\n📋 Opening CROPPED TABLE")

            print("\nOCR Text:")
            print("--------------------------------")
            print(document.metadata.get("ocr_text", ""))
            print("--------------------------------")

        # ==========================================
        # Fallback → Full Page
        # ==========================================

        else:

            table_path = document.metadata.get("page_image")

            print("\n📄 Opening FULL PAGE")

        if not table_path:

            print("\n❌ No table available.")

            return

        if not os.path.exists(table_path):

            print(f"\n❌ File not found:\n{table_path}")

            return

        print(f"\nOpening:\n{table_path}")

        img = Image.open(table_path)

        img.show()

        print("\n✅ Table displayed successfully.")