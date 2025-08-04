from pdf_processor import PDFProcessor
from glob import glob
from os import path
from docx import Document

# Set path to folder with your PDFs
PATH_PDFS = path.join(path.dirname(__file__), "speeches")

OUTPUT_FOLDER = path.join(path.dirname(__file__), "nepali_transcript")

def get_pdfs(path_dir):
    return glob(path.join(path_dir, "*.pdf"))

def save_text_to_docx(text, filename):
    """Save given text to a .docx."""
    filepath = path.join(OUTPUT_FOLDER, filename)
    doc = Document()
    for line in text.splitlines():
        doc.add_paragraph(line)
    doc.save(filepath)

if __name__ == "__main__":
    pdf_paths = get_pdfs(PATH_PDFS)
    print(f"Found {len(pdf_paths)} PDF files.")

    for pdf_path in pdf_paths:

        original_filename = path.basename(pdf_path)
        base_filename = path.splitext(original_filename)[0]

        try:
            text_pymupdf, _ = PDFProcessor.extract_text_with_pymupdf(pdf_path)
            save_text_to_docx(text_pymupdf, f"{base_filename}.docx")
            print(f"✅ Saved: {base_filename}.docx")
        except Exception as e:
            print(f"[Error - pymupdf] {pdf_path}: {e}")
