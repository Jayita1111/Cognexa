import cv2
import pytesseract
import pandas as pd


def get_confidence(image_path):
    image = cv2.imread(image_path)

    data = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DATAFRAME
    )

    data = data.dropna(subset=["text"])
    data = data[data["conf"] >= 0]

    return data["conf"].mean()


before_image = "images/original/K2_page_1.png"
after_image = "images/preprocessed/K2_preprocessed.png"

before_conf = get_confidence(before_image)
after_conf = get_confidence(after_image)

print("--------------------------------")
print("K2 OCR CONFIDENCE COMPARISON")
print("--------------------------------")

print(f"Before preprocessing : {before_conf:.2f}%")
print(f"After preprocessing  : {after_conf:.2f}%")

difference = after_conf - before_conf

print(f"Difference           : {difference:.2f} percentage points")

if difference > 0:
    print("Result: OCR confidence increased.")
elif difference < 0:
    print("Result: OCR confidence decreased.")
else:
    print("Result: OCR confidence remained the same.")