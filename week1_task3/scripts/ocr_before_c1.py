import cv2
import pytesseract
import os

image_path = "images/original/C1_page_1.png"

output_folder = "output/before_ocr"
os.makedirs(output_folder, exist_ok=True)

image = cv2.imread(image_path)

text = pytesseract.image_to_string(image)

output_file = os.path.join(
    output_folder,
    "C1_before.txt"
)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)

print("C1 BEFORE preprocessing OCR completed.")
print("OCR result saved to:", output_file)