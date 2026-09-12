# import os
# import fitz
# from PIL import Image
# from doclayout_yolo import YOLOv10


# # Load model only once
# model = YOLOv10(
#     "DocLayout-YOLO/weights/doclayout_yolo_docstructbench_imgsz1024.pt"
# )


# def extract_figures(page_image_path, pdf_name, page_number):

#     output_dir = "cropped_figures"
#     os.makedirs(output_dir, exist_ok=True)

#     results = model.predict(
#         page_image_path,
#         imgsz=1024,
#         conf=0.05,
#         save=False
#     )

#     image = Image.open(page_image_path)

#     figure_paths = []

#     for result in results:

#         boxes = result.boxes.xyxy.cpu().numpy()
#         classes = result.boxes.cls.cpu().numpy()

#         for i, cls in enumerate(classes):
#             print(
#               "Detected:",
#               class_name
#             )
#             class_name = model.names[int(cls)]

#             if class_name.lower() != "figure":
#                 continue

#             x1, y1, x2, y2 = boxes[i]

#             crop = image.crop((x1, y1, x2, y2))

#             figure_name = (
#                 f"{os.path.splitext(pdf_name)[0]}"
#                 f"_page_{page_number}"
#                 f"_fig_{i+1}.png"
#             )

#             figure_path = os.path.join(
#                 output_dir,
#                 figure_name
#             )

#             crop.save(figure_path)

#             figure_paths.append({
#              "path": figure_path,
#              "bbox": [float(x1), float(y1), float(x2), float(y2)]
#             })

#     return figure_paths
import os
from PIL import Image
from doclayout_yolo import YOLOv10
from src.ocr import extract_text


# =====================================================
# Load DocLayout-YOLO Model Once
# =====================================================

model = YOLOv10(
    "DocLayout-YOLO/weights/doclayout_yolo_docstructbench_imgsz1024.pt"
)


# =====================================================
# Extract Figures + OCR
# =====================================================

def extract_figures(page_image_path, pdf_name, page_number):

    output_dir = "cropped_figures"
    os.makedirs(output_dir, exist_ok=True)

    results = model.predict(
        page_image_path,
        imgsz=1024,
        conf=0.05,
        save=False
    )

    image = Image.open(page_image_path)

    figure_paths = []

    for result in results:

        boxes = result.boxes.xyxy.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy()

        for i, cls in enumerate(classes):

            class_name = model.names[int(cls)]

            print(f"Detected : {class_name}")

            # -----------------------------------------
            # Only keep useful regions
            # -----------------------------------------

            if class_name.lower() not in [
                "figure",
                "table"
                
            ]:
                continue

            x1, y1, x2, y2 = boxes[i]

            crop = image.crop((x1, y1, x2, y2))

            filename = (
                f"{os.path.splitext(pdf_name)[0]}"
                f"_page_{page_number}_"
                f"{class_name}_{i+1}.png"
            )

            save_path = os.path.join(
                output_dir,
                filename
            )

            crop.save(save_path)

            # -----------------------------------------
            # OCR
            # -----------------------------------------

            try:

                ocr_text = extract_text(save_path)

            except Exception as e:

                print("OCR Error :", e)

                ocr_text = ""

            print("\n📄 OCR TEXT")
            print("--------------------------------")

            if ocr_text.strip():

                print(ocr_text)

            else:

                print("No text detected")

            print("--------------------------------")

            figure_paths.append({

                "path": save_path,

                "bbox": [

                    float(x1),
                    float(y1),
                    float(x2),
                    float(y2)

                ],

                "class": class_name,

                "ocr_text": ocr_text,
                "number" : i + 1

            })

    return figure_paths