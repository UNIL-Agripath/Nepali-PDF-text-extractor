import os
import re
import pandas as pd
from docx import Document

# Folder where .docx files are stored
INPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'nepali_transcript')
AGRIPATH_FOLDER = os.path.join(os.path.dirname(__file__), 'Agripath')
os.makedirs(AGRIPATH_FOLDER, exist_ok=True)
OUTPUT_FILE = os.path.join(AGRIPATH_FOLDER, 'extracted_speeches.xlsx')


# Pattern for Nepali date: e.g., १८ फागुन २०८१
NEPALI_DATE_PATTERN = re.compile(r'\d{1,2} [\u0900-\u097F]+ २०[४-९]\d')

# Pattern to identify speaker headers
SPEAKER_PATTERN = re.compile(r'(माननीय\s*(श्री)?\s*[^\n\(：:–]{2,100}(?:\([^)]*\))?\s*[ः:：–]+)')



def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = '\n'.join([para.text.strip() for para in doc.paragraphs if para.text.strip()])
    return full_text


def extract_date(text):
    match = NEPALI_DATE_PATTERN.search(text)
    return match.group(0) if match else None


def extract_speeches(text):
    speeches = []
    date = extract_date(text)

    # Split based on speaker markers
    parts = SPEAKER_PATTERN.split(text)
    speakers = SPEAKER_PATTERN.findall(text)

    for i, speech in enumerate(parts[1:], start=0):
        speaker = speakers[i].replace("：", ":").replace(":", "").strip()
        speech_text = speech.strip()
        if speaker and speech_text:
            speeches.append({
                'Date': date,
                'Speaker': speaker,
                'Speech': speech_text
            })
    return speeches


def main():
    all_data = []

    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith('.docx'):
            file_path = os.path.join(INPUT_FOLDER, filename)
            print(f"📄 Processing: {filename}")
            try:
                text = extract_text_from_docx(file_path)
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
