import fitz
import os

pdf_path = "dataset/college/C3.pdf"
output_folder = "images/original"

os.makedirs(output_folder, exist_ok=True)

doc = fitz.open(pdf_path)

page = doc[0]

pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

output_path = os.path.join(output_folder, "C3_page_1.png")

pix.save(output_path)

print("C3 PDF converted to image successfully.")
print("Saved:", output_path)