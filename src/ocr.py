import torch
torch.set_num_threads(1)

import gc
import easyocr

reader = easyocr.Reader(['en'], gpu=False)


def extract_text(image_path):
    """
    Extract text from a cropped figure/image.
    """

    results = reader.readtext(image_path)

    text = " ".join([r[1] for r in results])

    gc.collect()

    return text.strip()

import easyocr

# Load once
reader = easyocr.Reader(['en'], gpu=False)


def extract_text(image_path):
    """
    Extract text from a cropped figure/image.
    """

    results = reader.readtext(image_path)

    text = " ".join([r[1] for r in results])

    return text.strip()
if __name__ == "__main__":
    text = extract_text(
        r"cropped_figures\MACHINE LEARNING_page_7_figure_1.png"
    )
    print(text)