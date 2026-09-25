from docx import Document
from docx.shared import Pt

doc = input("enter doc path: ")
Document = Document(doc) 

count = 0

for para in Document.paragraphs:
    for run in para.runs:
        if run.text == "." and run.font.size == Pt(2):
            count += 1

print(f"dot count in {doc} : {count}")
