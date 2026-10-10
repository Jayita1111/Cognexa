from pdf2image import convert_from_path
import os

pdf_path = "dataset/kaggle/K3.pdf"

output_folder = "images/original"
os.makedirs(output_folder, exist_ok=True)

pages = convert_from_path(pdf_path, dpi=300)

for i, page in enumerate(pages):
    output_path = f"{output_folder}/K3_page_{i+1}.png"
    page.save(output_path)
    print(f"Saved: {output_path}")

print("K3 PDF converted to image successfully.")