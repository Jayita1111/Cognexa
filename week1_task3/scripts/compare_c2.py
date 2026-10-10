import pytesseract
import cv2

# Original image
original_path = "images/original/C2_page_1.png"

# Preprocessed image
processed_path = "images/preprocessed/C2_preprocessed.png"

# Read images
original = cv2.imread(original_path)
processed = cv2.imread(processed_path)

# Get OCR data with confidence
before_data = pytesseract.image_to_data(
    original,
    output_type=pytesseract.Output.DICT
)

after_data = pytesseract.image_to_data(
    processed,
    output_type=pytesseract.Output.DICT
)

# Calculate average confidence
before_conf = [
    float(c)
    for c in before_data["conf"]
    if float(c) >= 0
]

after_conf = [
    float(c)
    for c in after_data["conf"]
    if float(c) >= 0
]

before_avg = sum(before_conf) / len(before_conf)
after_avg = sum(after_conf) / len(after_conf)

difference = after_avg - before_avg

print("==============================")
print("C2 OCR CONFIDENCE COMPARISON")
print("==============================")
print(f"Before preprocessing : {before_avg:.2f}%")
print(f"After preprocessing  : {after_avg:.2f}%")
print(f"Difference            : {difference:+.2f} percentage points")

if difference > 0:
    print("Result: OCR confidence increased.")
elif difference < 0:
    print("Result: OCR confidence decreased.")
else:
    print("Result: OCR confidence remained the same.")