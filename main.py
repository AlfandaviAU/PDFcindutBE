import os

from pypdf import PdfMerger

pdfs = ["test/Page 1.pdf","test/Page 2.pdf"]

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("result.pdf")
merger.close()