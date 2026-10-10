import cv2
import pytesseract
import os

image_path = "images/original/C2_page_1.png"

output_folder = "output/before_ocr"
os.makedirs(output_folder, exist_ok=True)

image = cv2.imread(image_path)

text = pytesseract.image_to_string(image)

output_file = os.path.join(
    output_folder,
    "C2_before.txt"
)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)

print("C2 BEFORE preprocessing OCR completed.")
print("OCR result saved to:", output_file)