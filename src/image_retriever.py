import os
from PIL import Image


class ImageRetriever:

    def __init__(self):
        pass

    def show_image(self, document):

        print("\n" + "=" * 60)
        print("IMAGE RETRIEVER")
        print("=" * 60)     

        print(f"PDF  : {document.metadata.get('source')}")
        print(f"Page : {document.metadata.get('page')}")

        image_path = None

        # ==========================================
        # Figure Retrieval (Highest Priority)
        # ==========================================

        if document.metadata.get("type") == "figure":

            image_path = document.metadata.get("figure_path")

            print("\n📊 Opening CROPPED FIGURE")

            print("OCR Text:")
            print(document.metadata.get("ocr_text", ""))

        # ==========================================
        # PDF Image Retrieval
        # ==========================================

        elif document.metadata.get("type") == "image":

            image_path = document.metadata.get("image_path")

            print("\n🖼 Opening CROPPED IMAGE")

        # ==========================================
        # Fallback → Full Page
        # ==========================================

        else:

            image_path = document.metadata.get("page_image")

            print("\n📄 Opening FULL PAGE")

        if not image_path:

            print("\n❌ No image available.")

            return

        if not os.path.exists(image_path):

            print(f"\n❌ File not found:\n{image_path}")

            return

        print(f"\nOpening:\n{image_path}")
        print("\n========== METADATA ==========")
        print(document.metadata)
        print("==============================")
        
        img = Image.open(image_path)

        img.show()

        print("\n✅ Image displayed successfully.")