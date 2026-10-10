import cv2
import pytesseract


def get_ocr_confidence(image_path):
    image = cv2.imread(image_path)

    data = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DICT
    )

    confidences = []

    for conf in data["conf"]:
        try:
            conf = float(conf)
            if conf >= 0:
                confidences.append(conf)
        except ValueError:
            pass

    if not confidences:
        return 0.0

    return sum(confidences) / len(confidences)


# Original image
before_image = "images/original/C1_page_1.png"

# Preprocessed image
after_image = "images/preprocessed/C1_preprocessed.png"


# Calculate confidence
before_confidence = get_ocr_confidence(before_image)
after_confidence = get_ocr_confidence(after_image)

difference = after_confidence - before_confidence


print("--------------------------------")
print("C1 OCR CONFIDENCE COMPARISON")
print("--------------------------------")

print(f"Before preprocessing : {before_confidence:.2f}%")
print(f"After preprocessing  : {after_confidence:.2f}%")
print(f"Difference           : {difference:+.2f} percentage points")

if difference > 0:
    print("Result: OCR confidence increased.")
elif difference < 0:
    print("Result: OCR confidence decreased.")
else:
    print("Result: OCR confidence remained unchanged.")