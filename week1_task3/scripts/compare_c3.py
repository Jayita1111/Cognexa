import pytesseract
from PIL import Image


def get_confidence(image_path):
    data = pytesseract.image_to_data(
        Image.open(image_path),
        output_type=pytesseract.Output.DICT
    )

    confidences = []

    for conf in data["conf"]:
        try:
            conf = float(conf)
            if conf > 0:
                confidences.append(conf)
        except ValueError:
            pass

    if confidences:
        return sum(confidences) / len(confidences)

    return 0


before_image = "images/original/C3_page_1.png"
after_image = "images/preprocessed/C3_preprocessed.png"

before = get_confidence(before_image)
after = get_confidence(after_image)

difference = after - before

print("==============================")
print("C3 OCR CONFIDENCE COMPARISON")
print("==============================")
print(f"Before preprocessing : {before:.2f}%")
print(f"After preprocessing  : {after:.2f}%")
print(f"Difference            : {difference:+.2f} percentage points")

if difference > 0:
    print("Result: OCR confidence increased.")
elif difference < 0:
    print("Result: OCR confidence decreased.")
else:
    print("Result: OCR confidence remained unchanged.")