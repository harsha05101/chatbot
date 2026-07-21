import io
import os
import shutil
from PIL import Image
import pytesseract

# Path to the Tesseract executable on Windows
tesseract_win_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

if os.name == 'nt' and os.path.exists(tesseract_win_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_win_path
elif shutil.which("tesseract"):
    pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract")


class OCRProcessor:

    @staticmethod
    def extract_text(image_bytes: bytes) -> str:
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode not in ('L', 'RGB'):
                img = img.convert('RGB')
            text = pytesseract.image_to_string(img)
            return text.strip()
        except Exception as e:
            print(f"[OCR Error]: {e}")
            return ""