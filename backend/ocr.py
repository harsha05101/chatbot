import io
import os
import shutil
from PIL import Image
import pytesseract
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Explicit path to Windows Tesseract executable
tesseract_win_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

if os.name == 'nt' and os.path.exists(tesseract_win_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_win_path
elif shutil.which('tesseract'):
    pytesseract.pytesseract.tesseract_cmd = shutil.which('tesseract')


class OCRProcessor:

    @staticmethod
    def extract_text(image_bytes: bytes) -> str:
        # --- 1. Try Local Tesseract First ---
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode not in ('L', 'RGB'):
                img = img.convert('RGB')
            text = pytesseract.image_to_string(img).strip()
            if text:
                return text
        except Exception as e:
            print(f'[Tesseract OCR Warning]: {e}. Falling back to Gemini Vision...')

        # --- 2. Fallback to Gemini Vision API (For Render Cloud) ---
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                print('[OCR Error]: GEMINI_API_KEY missing in environment variables.')
                return ''

            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
                    "Extract all text from this image exactly as it appears. If no legible text exists, respond with 'NO_TEXT_FOUND'."
                ]
            )

            extracted_text = response.text.strip()
            if "NO_TEXT_FOUND" in extracted_text:
                return ''
            return extracted_text

        except Exception as e:
            print(f'[Gemini OCR Error]: {e}')
            return ''