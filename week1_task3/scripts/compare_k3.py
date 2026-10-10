import cv2
import pytesseract

# Original image
before_image = cv2.imread("images/original/K3_page_1.png")

# Preprocessed image
after_image = cv2.imread("images/preprocessed/K3_preprocessed.png")

# Get OCR data with confidence
before_data = pytesseract.image_to_data(
    before_image,
    output_type=pytesseract.Output.DICT
)

after_data = pytesseract.image_to_data(
    after_image,
    output_type=pytesseract.Output.DICT
)


def calculate_confidence(data):
    confidences = []

    for conf in data["conf"]:
        try:
            value = float(conf)

            if value >= 0:
                confidences.append(value)

        except ValueError:
            pass

    if len(confidences) == 0:
        return 0

    return sum(confidences) / len(confidences)


before_confidence = calculate_confidence(before_data)
after_confidence = calculate_confidence(after_data)

difference = after_confidence - before_confidence

print("--------------------------------")
print("K3 OCR CONFIDENCE COMPARISON")
print("--------------------------------")

print(f"Before preprocessing : {before_confidence:.2f}%")
print(f"After preprocessing  : {after_confidence:.2f}%")
print(f"Difference            : {difference:+.2f} percentage points")

if difference > 0:
    print("Result: OCR confidence increased.")
elif difference < 0:
    print("Result: OCR confidence decreased.")
else:
    print("Result: OCR confidence remained the same.")