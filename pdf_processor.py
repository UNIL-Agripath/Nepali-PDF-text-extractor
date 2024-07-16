import pytesseract
from pdf2image import convert_from_path
import tempfile
from googletrans import Translator
from config import DEFAULT_LANGUAGE, DEFAULT_TARGET_LANGUAGE, PDF_TO_IMAGE_FORMAT

class PDFProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_path, language=DEFAULT_LANGUAGE):
        try:
            all_text = ""
            all_boxes = []
            
            with tempfile.TemporaryDirectory() as path:
                images = convert_from_path(pdf_path, output_folder=path, fmt=PDF_TO_IMAGE_FORMAT, use_pdftocairo=True)
                
                for i, image in enumerate(images):
                    width, height = image.size
                    data = pytesseract.image_to_data(image, lang=language, output_type=pytesseract.Output.DICT)
                    text = " ".join(data['text'])
                    all_text += f"Page {i+1}:\n{text}\n\n"
                    
                    boxes = []
                    for j in range(len(data['text'])):
                        if int(data['conf'][j]) > 60:
                            (x, y, w, h) = (data['left'][j], data['top'][j], data['width'][j], data['height'][j])
                            # Store coordinates as ratios of page dimensions
                            boxes.append((x/width, y/height, w/width, h/height, data['text'][j]))
                    
                    all_boxes.append(boxes)
            
            return all_text, all_boxes
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")


    @staticmethod
    def translate_text(text, target_language=DEFAULT_TARGET_LANGUAGE):
        try:
            translator = Translator()
            translated = translator.translate(text, dest=target_language)
            return translated.text
        except Exception as e:
            raise Exception(f"Error translating text: {str(e)}")