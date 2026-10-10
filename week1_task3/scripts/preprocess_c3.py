import cv2
import os

image_path = "images/original/C3_page_1.png"
output_folder = "images/preprocessed"

os.makedirs(output_folder, exist_ok=True)

image = cv2.imread(image_path)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (3, 3), 0)

_, thresh = cv2.threshold(
    blur,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

output_path = os.path.join(
    output_folder,
    "C3_preprocessed.png"
)

cv2.imwrite(output_path, thresh)

print("C3 preprocessing completed.")
print("Saved:", output_path)