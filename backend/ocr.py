import pytesseract
from PIL import Image
import io
import os
import shutil

# Check if running on Windows and explicit executable path exists
tesseract_win_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.name == 'nt' and os.path.exists(tesseract_win_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_win_path
elif shutil.which("tesseract"):
    # On Linux/Render, pytesseract automatically uses PATH if tesseract is installed
    pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract")

class OCRProcessor:
    @staticmethod
    def extract_text(image_bytes):
        try:
            img = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(img)
            return text.strip()
        except Exception as e:
            print(f"OCR Processing Error: {e}")
            return ""