import cv2
import pytesseract
import os

image_path = "images/preprocessed/K3_preprocessed.png"

output_folder = "output/after_ocr"
os.makedirs(output_folder, exist_ok=True)

image = cv2.imread(image_path)

text = pytesseract.image_to_string(image)

output_file = os.path.join(
    output_folder,
    "K3_after.txt"
)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)

print("K3 AFTER preprocessing OCR completed.")
print("OCR result saved to:", output_file)