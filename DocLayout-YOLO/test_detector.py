import os
from PIL import Image
from doclayout_yolo import YOLOv10

model = YOLOv10("weights/doclayout_yolo_docstructbench_imgsz1024.pt")

image_path = r"C:\Users\Himanshu Vyas\Desktop\PDF_Chatbot\page_images\MACHINE LEARNING_page_1.png"

results = model.predict(
    source=image_path,
    imgsz=1024,
    conf=0.25
)

os.makedirs("cropped_figures", exist_ok=True)

image = Image.open(image_path)

for result in results:

    boxes = result.boxes

    names = result.names

    for i, box in enumerate(boxes):

        cls = int(box.cls[0])

        label = names[cls]

        if label == "figure":

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            crop = image.crop((x1, y1, x2, y2))

            output_path = f"cropped_figures/figure_{i}.png"

            crop.save(output_path)

            print(f"Saved -> {output_path}")