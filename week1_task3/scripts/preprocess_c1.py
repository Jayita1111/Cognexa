import cv2
import os

input_path = "images/original/C1_page_1.png"
output_folder = "images/preprocessed"

os.makedirs(output_folder, exist_ok=True)

image = cv2.imread(input_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Remove noise
denoised = cv2.GaussianBlur(gray, (3, 3), 0)

# Convert to binary image
_, binary = cv2.threshold(
    denoised,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

output_path = os.path.join(
    output_folder,
    "C1_preprocessed.png"
)

cv2.imwrite(output_path, binary)

print("C1 preprocessing completed.")
print("Saved:", output_path)