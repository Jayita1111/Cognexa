import cv2
import os

# Input image
input_path = "images/original/K1_page_1.png"

# Output folder
output_folder = "images/preprocessed"
os.makedirs(output_folder, exist_ok=True)

# Read image
image = cv2.imread(input_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Remove small noise
blur = cv2.GaussianBlur(gray, (3, 3), 0)

# Apply Otsu thresholding
_, threshold = cv2.threshold(
    blur,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

# Save preprocessed image
output_path = os.path.join(
    output_folder,
    "K1_preprocessed.png"
)

cv2.imwrite(output_path, threshold)

print("K1 preprocessing completed.")
print(f"Saved: {output_path}")