# Nepali PDF Text Extractor and Translator

This application provides a graphical user interface (GUI) for extracting and comparing text from PDF files in Nepali using various libraries and translating the extracted text to English.

## Features

- Extract text from PDF files in Nepali language
- Compare text extraction results from multiple libraries:
  - pytesseract
  - pdfplumber
  - PyMuPDF (fitz)
  - PyPDF2
- Translate extracted Nepali text to English
- User-friendly GUI built with tkinter

## Installation

1. Clone this repository:
https://github.com/rasik-nep/Nepali-PDF-text-extractor.git

2. Install the required dependencies:
pip install -r requirements.txt

## Usage

1. Run the application:
python main.py

2. Use the GUI to:
- Select a PDF file
- Choose the text extraction library
- Extract text
- View extraction results
- Translate text to English

## Libraries Used

- **pytesseract**: Optical Character Recognition (OCR) tool for Python
- **pdfplumber**: PDF parsing and data extraction library
- **PyMuPDF (fitz)**: PDF rendering and analysis library
- **PyPDF2**: PDF processing library
- **googletrans**: Python library for Google Translate API

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Using pytesseract
You'll also need to install Tesseract OCR on your system. You can download it from [here](https://github.com/tesseract-ocr/tesseract).
Ensure that you have the Nepali language data for Tesseract. You can download it from [here](https://github.com/tesseract-ocr/tessdata).
