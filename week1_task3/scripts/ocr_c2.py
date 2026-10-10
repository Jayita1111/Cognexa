import fitz
import os

pdf_path = "dataset/college/C2.pdf"
output_folder = "images/original"

os.makedirs(output_folder, exist_ok=True)

doc = fitz.open(pdf_path)

for page_number, page in enumerate(doc):
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

    output_path = os.path.join(
        output_folder,
        f"C2_page_{page_number + 1}.png"
    )

    pix.save(output_path)

print("C2 PDF converted to image successfully.")