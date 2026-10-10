import cv2
import pytesseract
import os

# Preprocessed image
image_path = "images/preprocessed/C2_preprocessed.png"

# Output folder
output_folder = "output/after_ocr"
os.makedirs(output_folder, exist_ok=True)

# Read image
image = cv2.imread(image_path)

# OCR
text = pytesseract.image_to_string(image)

# Save OCR result
output_file = os.path.join(
    output_folder,
    "C2_after.txt"
)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)

print("C2 AFTER preprocessing OCR completed.")
print("OCR result saved to:", output_file)