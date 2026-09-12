import os
import fitz
import pdfplumber

from src.layout_detector import extract_figures


def _build_page_text(text_blocks):
    return "\n".join(
        block.get("text", "")
        for block in text_blocks
        if block.get("text", "").strip()
    )


# ==========================================================
# EXTRACT ORIGINAL INDIVIDUAL IMAGES FROM PDF
# ==========================================================

def extract_pdf_images(page, pdf_name, page_number):

    image_dir = "extracted_images"
    os.makedirs(image_dir, exist_ok=True)

    images = []

    image_list = page.get_images(full=True)

    for img_no, img in enumerate(image_list):

        xref = img[0]

        try:

            pix = fitz.Pixmap(page.parent, xref)

            image_name = (
                f"{os.path.splitext(pdf_name)[0]}"
                f"_page_{page_number}"
                f"_image_{img_no+1}.png"
            )

            image_path = os.path.join(
                image_dir,
                image_name
            )

            if pix.n - pix.alpha < 4:
                pix.save(image_path)
            else:
                rgb_pix = fitz.Pixmap(fitz.csRGB, pix)
                rgb_pix.save(image_path)
                rgb_pix = None

            images.append(image_path)

            print("\n🖼️ IMAGE EXTRACTED")
            print("----------------------")
            print("PDF       :", pdf_name)
            print("Page      :", page_number)
            print("Image No. :", img_no + 1)
            print("Path      :", image_path)

            pix = None

        except Exception as e:

            print(f"Image extraction failed Page {page_number}: {e}")

    return images


# ==========================================================
# LOAD ALL PDFs
# ==========================================================

def load_all_pdfs(folder_path):

    all_pdfs = []

    pdf_files = [
        f
        for f in os.listdir(folder_path)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:
        print("⚠ No PDFs Found")
        return []

    print(f"\n📂 Found {len(pdf_files)} PDFs")

    os.makedirs("page_images", exist_ok=True)

    for pdf_file in pdf_files:

        pdf_path = os.path.join(folder_path, pdf_file)

        print("\n" + "=" * 60)
        print(f"📄 Loading : {pdf_file}")
        print("=" * 60)

        document = fitz.open(pdf_path)

        pages = []

        total_tables = 0
        total_images = 0
        page_text_character_count = 0

        with pdfplumber.open(pdf_path) as plumber_pdf:

            for page_number, page in enumerate(document, start=1):

                # ==========================================
                # TEXT BLOCKS
                # ==========================================

                blocks = []

                for block in page.get_text("blocks"):

                    if len(block) < 5:
                        continue

                    x0, y0, x1, y1, text = block[:5]

                    if not text.strip():
                        continue

                    blocks.append({

                        "text": text,

                        "bbox": [
                            x0,
                            y0,
                            x1,
                            y1
                        ]
                    })

                page_text = _build_page_text(blocks)

                page_text_character_count += len(page_text)

                # ==========================================
                # TABLE EXTRACTION (pdfplumber)
                # ==========================================

                raw_tables = []

                try:

                    plumber_page = plumber_pdf.pages[
                        page_number - 1
                    ]

                    extracted_tables = plumber_page.extract_tables()

                    if extracted_tables:

                        for table in extracted_tables:

                            table_text = ""

                            for row in table:

                                row = [
                                    cell if cell else ""
                                    for cell in row
                                ]

                                table_text += (
                                    " | ".join(row)
                                    + "\n"
                                )

                            raw_tables.append(table_text)

                except Exception:
                    pass

                # ==========================================
                # SAVE PAGE IMAGE
                # ==========================================

                pix = page.get_pixmap(
                    matrix=fitz.Matrix(2, 2)
                )

                page_image_name = (
                    f"{os.path.splitext(pdf_file)[0]}"
                    f"_page_{page_number}.png"
                )

                page_image_path = os.path.join(
                    "page_images",
                    page_image_name
                )

                pix.save(page_image_path)

                # ==========================================
                # ORIGINAL PDF IMAGES
                # ==========================================

                images = extract_pdf_images(
                    page,
                    pdf_file,
                    page_number
                )

                total_images += len(images)

                # ==========================================
                # YOLO LAYOUT DETECTION
                # ==========================================

                layout_items = extract_figures(
                    page_image_path,
                    os.path.splitext(pdf_file)[0],
                    page_number
                )

                figures = [
                    item
                    for item in layout_items
                    if item["class"].lower() == "figure"
                ]

                detected_tables = [
                    item
                    for item in layout_items
                    if item["class"].lower() == "table"
                ]

                print(f"\nYOLO Found {len(figures)} Figures")
                print(f"YOLO Found {len(detected_tables)} Tables")

                total_tables += len(detected_tables)

                # ==========================================
                # STORE PAGE
                # ==========================================

                pages.append({

                    "page": page_number,

                    "text": page_text,

                    "text_blocks": blocks,

                    "tables": detected_tables,

                    "raw_tables": raw_tables,

                    "images": images,

                    "figures": figures,

                    "page_image": page_image_path,

                    "page_metadata": {

                        "source": pdf_file,

                        "page_number": page_number,

                        "text_length": len(page_text),

                        "image_count": len(images),

                        "figure_count": len(figures),

                        "table_count": len(detected_tables)

                    }

                })

        all_pdfs.append({

            "file_name": pdf_file,

            "pages": len(document),

            "content": pages,

            "total_images": total_images,

            "total_tables": total_tables,

            "text_characters": page_text_character_count,

            "page_count": len(pages)

        })

        print(f"✅ Pages Loaded      : {len(document)}")
        print(f"🖼 Images Extracted  : {total_images}")
        print(f"📊 Tables Found      : {total_tables}")

        document.close()

    print("\n✅ All PDFs Loaded Successfully!\n")

    return all_pdfs