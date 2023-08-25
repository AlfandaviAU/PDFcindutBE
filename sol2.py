import os
from PyPDF2 import PdfMerger, PdfReader
import shutil
from PyPDF2 import PdfMerger
from flask_cors import CORS
import zipfile

def merge_pdfs_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        if len(os.path.basename(root)) >= 4:
            merger = PdfMerger()

            for filename in files:
                if filename.endswith(".pdf"):
                    filepath = os.path.join(root, filename)
                    merger.append(PdfReader(filepath), import_outline=False)
                    os.remove(filepath)
            output_directory = os.path.join(root)
            os.makedirs(output_directory, exist_ok=True)

            output_filename = os.path.join(output_directory, "Merged.pdf")
            merger.write(output_filename)
            merger.close()
            print(f"Merged PDFs saved as {output_filename}")

def main():
    with zipfile.ZipFile("RJ.zip", 'r') as zip_ref:
        zip_ref.extractall("RJ")

    print("PDF merging script")
    merge_pdfs_in_directory("RJ")

if __name__ == "__main__":
    main()
