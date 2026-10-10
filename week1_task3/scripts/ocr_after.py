import cv2
import pytesseract
import os

# Preprocessed image
image_path = "images/preprocessed/K1_preprocessed.png"

# Output folder
output_folder = "output/after_ocr"
os.makedirs(output_folder, exist_ok=True)

# Read preprocessed image
image = cv2.imread(image_path)

# OCR
text = pytesseract.image_to_string(image)

# Save OCR result
output_file = os.path.join(output_folder, "K1_after.txt")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)

print("AFTER preprocessing OCR completed.")
print(f"OCR result saved to: {output_file}")