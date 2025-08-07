import os
import re
import pandas as pd
import fitz  # PyMuPDF

# Folder containing the PDF files
INPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'speeches')
AGRIPATH_FOLDER = os.path.join(os.path.dirname(__file__), 'Agripath')
os.makedirs(AGRIPATH_FOLDER, exist_ok=True)
OUTPUT_FILE = os.path.join(AGRIPATH_FOLDER, 'extracted_speeches.xlsx')

# Nepali date pattern
NEPALI_DATE_PATTERN = re.compile(r'\d{1,2} [\u0900-\u097F]+ २०[४-९]\d')

# Pattern to identify speech blocks
SPEECH_START_PATTERN = re.compile(r'(माननीय|सम्माननीय)\s*(श्री)?\s*[^\n]{2,100}?[：:–-]')

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_date(text):
    match = NEPALI_DATE_PATTERN.search(text)
    return match.group(0) if match else None


def extract_speeches(text):
    date = extract_date(text)
    speeches = []

    # Split text by speech markers (माननीय or सम्माननीय)
    speech_split_pattern = re.compile(r'(माननीय|सम्माननीय)[^\n]{0,200}[:：–-]')
    matches = list(speech_split_pattern.finditer(text))

    for i, match in enumerate(matches):
        start_idx = match.end()

        if i + 1 < len(matches):
            end_idx = matches[i + 1].start()
        else:
            end_idx = len(text)

        speech_block = text[start_idx:end_idx].strip()

        # Try to extract speaker name from within that block
        name_match = re.search(r'(श्री|डा)\s*([^\n:：–-]{2,100})', text[match.start():match.end()])
        if name_match:
            speaker = f"{name_match.group(1)} {name_match.group(2).strip()}"
        else:
            speaker = "अज्ञात"

        # Trim at 'धन्यवाद।' if present
        thanks_match = re.search(r'धन्यवाद।', speech_block)
        if thanks_match:
            speech_block = speech_block[:thanks_match.end()]

        speeches.append({
            'Date': date,
            'Speaker': speaker,
            'Speech': speech_block
        })

    return speeches



def main():
    all_data = []

    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith('.pdf'):
            file_path = os.path.join(INPUT_FOLDER, filename)
            print(f"📄 Processing: {filename}")
            try:
                text = extract_text_from_pdf(file_path)
                print("🔍 Sample text:", text[:300])
                speech_data = extract_speeches(text)
                all_data.extend(speech_data)
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"✅ Data saved to: {OUTPUT_FILE}")
    else:
        print("⚠️ No data extracted.")


if __name__ == "__main__":
    main()
