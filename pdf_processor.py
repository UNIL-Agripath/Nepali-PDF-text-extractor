import pytesseract
from pdf2image import convert_from_path
import pdfplumber
import tempfile
from preeti_unicode import preeti 
import fitz  # PyMuPDF
from PyPDF2 import PdfReader

from googletrans import Translator
from config import DEFAULT_LANGUAGE, DEFAULT_TARGET_LANGUAGE, PDF_TO_IMAGE_FORMAT

class PDFProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_path, language=DEFAULT_LANGUAGE, boxes=False):
        try:
            all_text = ""
            if boxes:
                all_boxes = []

            # Advanced Tesseract configuration
            custom_config = r'--oem 3 --psm 6'
            
            with tempfile.TemporaryDirectory() as path:
                images = convert_from_path(pdf_path, output_folder=path, fmt=PDF_TO_IMAGE_FORMAT, use_pdftocairo=True)
                
                for i, image in enumerate(images):
                    width, height = image.size
                    
                    # Use advanced configuration in image_to_data
                    data = pytesseract.image_to_data(image, lang=language, output_type=pytesseract.Output.DICT, config=custom_config)
                    
                    text = " ".join(data['text'])
                    all_text += f"Page {i+1}:\n{text}\n\n"

                    if boxes:
                        boxes = []
                        for j in range(len(data['text'])):
                            if int(data['conf'][j]) > 60:
                                (x, y, w, h) = (data['left'][j], data['top'][j], data['width'][j], data['height'][j])
                                # Store coordinates as ratios of page dimensions
                                boxes.append((x/width, y/height, w/width, h/height, data['text'][j]))

                        all_boxes.append(boxes)
            if boxes:
                return all_text, all_boxes
            else:
                return all_text
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")


    @staticmethod
    def extract_text_with_pdfplumber(pdf_path):
        try:
            with pdfplumber.open(pdf_path) as pdf:
                all_text = ""
                all_boxes = []
                
                for page_num, page in enumerate(pdf.pages):
                    page_text = ""
                    page_boxes = []
                    words = page.extract_words()
                    
                    for word in words:
                        page_text += word['text'] + ' '
                        # Normalize coordinates
                        x0, top, x1, bottom = word['x0'], word['top'], word['x1'], word['bottom']
                        page_width, page_height = page.width, page.height
                        normalized_box = (
                            x0 / page_width,
                            top / page_height,
                            (x1 - x0) / page_width,  # width
                            (bottom - top) / page_height,  # height
                            word['text']
                        )
                        page_boxes.append(normalized_box)
                    
                    all_text += f"Page {page_num + 1}:\n{page_text}\n\n"
                    all_boxes.append(page_boxes)
                
            # encoding = PDFProcessor.detect_encoding(all_text)
            return preeti(all_text), all_boxes
        except Exception as e:
            raise Exception(f"Error extracting text with pdfplumber: {str(e)}")

    @staticmethod
    def extract_text_with_pymupdf(pdf_path):
        try:
            doc = fitz.open(pdf_path)
            all_text = ""
            all_boxes = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                page_text = page.get_text("text")
                all_text += f"Page {page_num + 1}:\n{page_text}\n\n"
                
                words = page.get_text("words")
                page_boxes = []
                for word in words:
                    x0, y0, x1, y1, text = word[:5]
                    width, height = page.rect.width, page.rect.height
                    normalized_box = (
                        x0 / width,
                        y0 / height,
                        (x1 - x0) / width,
                        (y1 - y0) / height,
                        text
                    )
                    page_boxes.append(normalized_box)
                all_boxes.append(page_boxes)
            
            return preeti(all_text), all_boxes
        except Exception as e:
            raise Exception(f"Error extracting text with PyMuPDF: {str(e)}")

    @staticmethod
    def extract_text_with_pypdf2(pdf_path):
        try:
            reader = PdfReader(pdf_path)
            all_text = ""
            
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                all_text += f"Page {page_num + 1}:\n{page_text}\n\n"
            
            return preeti(all_text), None  # PyPDF2 doesn't provide easy access to text coordinates
        except Exception as e:
            raise Exception(f"Error extracting text with PyPDF2: {str(e)}")

    @staticmethod   
    def translate_text(text, target_language=DEFAULT_TARGET_LANGUAGE):
        try:
            translator = Translator()
            translated = translator.translate(text, dest=target_language)
            return translated.text
        except Exception as e:
            raise Exception(f"Error translating text: {str(e)}")