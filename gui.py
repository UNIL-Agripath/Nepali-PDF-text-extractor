import tkinter as tk
from tkinter import filedialog, ttk
from pdf_processor import PDFProcessor
import fitz  # PyMuPDF
from PIL import Image, ImageTk, ImageDraw

class OCRApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Nepali OCR and Translator")
        self.root.geometry("1200x800")

        self.pdf_path = None
        self.current_page = 0
        self.pdf_document = None
        self.translations = {}  # Store translations
        self.bounding_boxes = []  # Store bounding boxes for each page

        self.setup_ui()


    def setup_ui(self):
        # Top frame for buttons
        top_frame = ttk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.select_button = ttk.Button(top_frame, text="Select PDF", command=self.select_pdf)
        self.select_button.pack(side=tk.LEFT, padx=5)

        self.load_button = ttk.Button(top_frame, text="Load Tessarcat", command=self.load_pdf)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        self.load_button = ttk.Button(top_frame, text="Load pdfplumber", command=self.load_pdf_pdfplumber)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        self.load_button = ttk.Button(top_frame, text="Load pymupdf", command=self.load_pdf_PyMuPDF)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        self.load_button = ttk.Button(top_frame, text="Load pypdf2", command=self.load_pdf_pypdf2)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        self.prev_button = ttk.Button(top_frame, text="Previous Page", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(top_frame, text="Next Page", command=self.next_page)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.translate_button = ttk.Button(top_frame, text="Translate Selection", command=self.translate_selection)
        self.translate_button.pack(side=tk.LEFT, padx=5)

        # Main content frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Left frame for PDF viewer
        self.pdf_frame = ttk.Frame(content_frame, width=600)
        self.pdf_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.pdf_canvas = tk.Canvas(self.pdf_frame, width=600, height=700)
        self.pdf_canvas.pack(expand=True, fill=tk.BOTH)

        # Right frame for extracted text
        text_frame = ttk.Frame(content_frame, width=600)
        text_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text_area = tk.Text(text_frame, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.text_area.bind("<ButtonRelease-1>", self.on_text_click)
        
        # Scrollbar for text area
        text_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_area.yview)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.configure(yscrollcommand=text_scrollbar.set)

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.pdf_path:
            self.pdf_document = fitz.open(self.pdf_path)
            
    def load_pdf(self):
        self.current_page = 0
        self.process_pdf(self.pdf_path)
        self.display_page()
    
    def load_pdf_pdfplumber(self):
        self.current_page = 0
        self.process_pdf_pdfplumber(self.pdf_path)
        self.display_page()
    
    def load_pdf_PyMuPDF(self):
        self.current_page = 0
        self.process_pdf_PyMuPDF(self.pdf_path)
        self.display_page()
        
    def load_pdf_pypdf2(self):
        self.current_page = 0
        self.process_pdf_pypdf2(self.pdf_path)
        self.display_page()
        
    def display_page(self):
        if self.pdf_document:
            page = self.pdf_document[self.current_page]
            zoom = 1.5  # Adjust this value to change the zoom level
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Draw bounding boxes
            draw = ImageDraw.Draw(img)
            if self.current_page < len(self.bounding_boxes):
                for box in self.bounding_boxes[self.current_page]:
                    x, y, w, h, _ = box
                    # Convert relative coordinates to absolute pixel coordinates
                    x1 = int(x * pix.width)
                    y1 = int(y * pix.height)
                    x2 = int((x + w) * pix.width)
                    y2 = int((y + h) * pix.height)
                    draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

            img.thumbnail((600, 700))
            photo = ImageTk.PhotoImage(img)
            self.pdf_canvas.config(width=photo.width(), height=photo.height())
            self.pdf_canvas.delete("all")
            self.pdf_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.pdf_canvas.image = photo

    def prev_page(self):
        if self.pdf_document and self.current_page > 0:
            self.current_page -= 1
            self.display_page()

    def next_page(self):
        if self.pdf_document and self.current_page < len(self.pdf_document) - 1:
            self.current_page += 1
            self.display_page()

    def process_pdf(self, pdf_path):
        extracted_text, self.bounding_boxes = PDFProcessor.extract_text_from_pdf(pdf_path)
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, extracted_text)

    def process_pdf_pdfplumber(self, pdf_path):
        extracted_text, self.bounding_boxes = PDFProcessor.extract_text_with_pdfplumber(pdf_path)
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, extracted_text)
    
    def process_pdf_PyMuPDF(self, pdf_path):
        extracted_text, self.bounding_boxes = PDFProcessor.extract_text_with_pymupdf(pdf_path)
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, extracted_text)
        
    def process_pdf_pypdf2(self, pdf_path):
        extracted_text, self.bounding_boxes = PDFProcessor.extract_text_with_pypdf2(pdf_path)
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, extracted_text)
        
    def translate_selection(self):
        try:
            selected_text = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected_text:
                translated_text = PDFProcessor.translate_text(selected_text)
                self.translations[selected_text] = translated_text
                self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
                self.text_area.insert(tk.INSERT, translated_text)
        except tk.TclError:
            # No selection
            pass

    def on_text_click(self, event):
        try:
            index = self.text_area.index(f"@{event.x},{event.y}")
            line_start = self.text_area.index(f"{index} linestart")
            line_end = self.text_area.index(f"{index} lineend")
            clicked_text = self.text_area.get(line_start, line_end)

            if clicked_text in self.translations:
                # Swap between Nepali and English
                self.text_area.delete(line_start, line_end)
                self.text_area.insert(line_start, self.translations[clicked_text])
                self.translations[self.translations[clicked_text]] = clicked_text
                del self.translations[clicked_text]
            else:
                # Select the entire sentence
                self.text_area.tag_remove(tk.SEL, "1.0", tk.END)
                self.text_area.tag_add(tk.SEL, line_start, line_end)
        except tk.TclError:
            pass

    def run(self):
        self.root.mainloop()