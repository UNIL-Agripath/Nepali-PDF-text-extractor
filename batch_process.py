from pdf_processor import PDFProcessor
from glob import glob
from os import path

PATH_PDFS = path.join(path.dirname(__file__), "speeches")

def get_pdfs(path_dir):
    """Retrieve all text from all PDFs."""
    paths_pdf = glob(path.join(path_dir, "*.pdf"))
    pdf_documents = []
    for path_pdf in paths_pdf:
        pdf_documents.append(PDFProcessor.extract_text_from_pdf(path_pdf))
    return pdf_documents

if __name__ == "__main__":
    pdf_documents = get_pdfs(PATH_PDFS)
    print("Imported text from", len(pdf_documents), " PDFs.")
    print(pdf_documents[0]) # first pdf
    print(pdf_documents[1]) # second pdf