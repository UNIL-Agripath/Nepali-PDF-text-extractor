import pytesseract
from pdf2image import convert_from_path
import tempfile
from googletrans import Translator

class PDFProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_path, language='nep'):
        try:
            all_text = ""
            
            with tempfile.TemporaryDirectory() as path:
                images = convert_from_path(pdf_path, output_folder=path, fmt='png', use_pdftocairo=True)
                
                for i, image in enumerate(images):
                    text = pytesseract.image_to_string(image, lang=language)
                    all_text += f"Page {i+1}:\n{text}\n\n"
            
            return all_text
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    @staticmethod
    def translate_text(text, target_language='en'):
        try:
            translator = Translator()
            translated = translator.translate(text, dest=target_language)
            return translated.text
        except Exception as e:
            raise Exception(f"Error translating text: {str(e)}")