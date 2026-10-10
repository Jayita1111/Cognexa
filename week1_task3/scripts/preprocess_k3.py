import cv2
import os

# Input image
image_path = "images/original/K3_page_1.png"

# Output folder
output_folder = "images/preprocessed"
os.makedirs(output_folder, exist_ok=True)

# Read image
image = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding
_, thresh = cv2.threshold(
    gray,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

# Save preprocessed image
output_path = os.path.join(
    output_folder,
    "K3_preprocessed.png"
)

cv2.imwrite(output_path, thresh)

print("K3 preprocessing completed.")
print("Saved:", output_path)