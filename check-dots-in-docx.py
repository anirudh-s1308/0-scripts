import re
from docx import Document
from docx.shared import Pt

doc_path = input("enter doc path: ")
doc = Document(doc_path)

total_qualifying_dots = 0

for num, para in enumerate(doc.paragraphs):
    # 1. Clean the paragraph text by ignoring any hidden 2pt dots
    # This prevents injected dots from inflating the sentence count
    clean_text = "".join(
        run.text for run in para.runs 
        if not (run.text == "." and run.font.size == Pt(2))
    ).strip()

    # 2. Count sentences using terminal punctuation clusters
    sentences = re.findall(r'[.!?]+(?:\s+|$)', clean_text)
    sentence_count = len(sentences)
    
    # Handle single line/heading with no ending punctuation
    if sentence_count == 0 and any(c.isalnum() for c in clean_text):
        sentence_count = 1

    # 3. Count 2pt dots in the current paragraph
    para_dot_count = 0
    for run in para.runs:
        if run.text == "." and run.font.size == Pt(2):
            para_dot_count += 1

    # 4. Only increment the document total if the paragraph has > 3 sentences
    if sentence_count >= 3:
        total_qualifying_dots += para_dot_count
        print(f"para {num} (sentences: {sentence_count}) -> dot count: {para_dot_count}")
    else:
        print(f"para {num} (sentences: {sentence_count} < 3) -> skipped (had {para_dot_count} dots)")

print(f"\nTotal 2pt dots in paragraphs with > 3 sentences in {doc_path} : {total_qualifying_dots}")