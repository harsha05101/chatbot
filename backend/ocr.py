import pytesseract
from PIL import Image
import io
import os

# Configure common default installation path for Tesseract on Windows
tesseract_win_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(tesseract_win_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_win_path

class OCRProcessor:
    @staticmethod
    def extract_text(image_bytes):
        try:
            img = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(img)
            return text.strip()
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""