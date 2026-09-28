import os
import re
from docx import Document
from docx.shared import Pt


def get_clean_para_text(paragraph):
    """Reconstructs paragraph text while ignoring injected 2pt dots

    so they do not artificially inflate sentence counts.
    """
    return "".join(
        run.text
        for run in paragraph.runs
        if not (run.text == "." and run.font.size == Pt(2))
    ).strip()


def count_sentences(text):
    """Counts sentences using punctuation clusters, handling trailing quotes/brackets."""
    if not text:
        return 0

    sentences = re.findall(r"[.!?]+['\"\)\]]*(?:\s+|$)", text)
    sentence_count = len(sentences)

    # Account for single line/heading without ending punctuation
    if sentence_count == 0 and any(c.isalnum() for c in text):
        sentence_count = 1

    return sentence_count


def count_dots_in_paragraph(paragraph):
    """Counts 2pt dot runs inserted into a paragraph."""
    count = 0
    for run in paragraph.runs:
        if run.text == "." and run.font.size == Pt(2):
            count += 1
    return count


def analyze_document(doc):
    """Analyzes all paragraphs in the document, logging dot counts for paragraphs

    with >= 3 sentences.
    """
    total_qualifying_dots = 0
    results_log = []

    for num, para in enumerate(doc.paragraphs, start=1):
        clean_text = get_clean_para_text(para)
        sentence_count = count_sentences(clean_text)
        para_dot_count = count_dots_in_paragraph(para)

        # Qualification threshold: paragraphs with >= 3 sentences
        if sentence_count >= 3:
            total_qualifying_dots += para_dot_count
            line = f"para {num} (sentences: {sentence_count}) -> dot count: {para_dot_count}"
            print(line)
            results_log.append(line)
        else:
            if para_dot_count > 0:
                print(
                    f"para {num} (sentences: {sentence_count} < 3) -> skipped (had {para_dot_count} dots)"
                )

    return total_qualifying_dots, results_log


def write_to_result(output_file, doc_path, total_dots, results_log):
    with open(output_file, "a", encoding="utf-8") as f:
        for line in results_log:
            f.write(line + "\n")
        f.write(
            f"\nTotal 2pt dots in paragraphs with >= 3 sentences in {doc_path} : {total_dots}\n"
        )
        f.write("-" * 80 + "\n")


def main():
    raw_path = input("Enter doc path: ").strip().strip('"').strip("'")
    if not os.path.exists(raw_path):
        print(f"Error: File not found at '{raw_path}'")
        return

    doc = Document(raw_path)
    total_dots, results_log = analyze_document(doc)

    output_path = "results.txt"
    write_to_result(output_path, raw_path, total_dots, results_log)
    print(f"\nDone. Total qualifying dots: {total_dots}. Log saved to {output_path}")


if __name__ == "__main__":
    main()