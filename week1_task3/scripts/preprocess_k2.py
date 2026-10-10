import cv2
import os

# Input image
input_path = "images/original/K2_page_1.png"

# Output folder
output_folder = "images/preprocessed"
os.makedirs(output_folder, exist_ok=True)

# Read image
image = cv2.imread(input_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Gaussian blur
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Otsu thresholding
_, thresh = cv2.threshold(
    blur,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

# Save preprocessed image
output_path = "images/preprocessed/K2_preprocessed.png"

cv2.imwrite(output_path, thresh)

print("K2 preprocessing completed.")
print(f"Saved: {output_path}")