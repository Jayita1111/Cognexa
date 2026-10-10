import cv2
import pytesseract
import os

# Input image
image_path = "images/original/K1_page_1.png"

# Output folder
output_folder = "output/before_ocr"
os.makedirs(output_folder, exist_ok=True)

# Read original image
image = cv2.imread(image_path)

# OCR on original image
text = pytesseract.image_to_string(image)

# Save OCR result
output_file = os.path.join(output_folder, "K1_before.txt")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)

print("BEFORE preprocessing OCR completed.")
print(f"OCR result saved to: {output_file}")