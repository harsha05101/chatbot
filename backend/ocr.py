import os
import io
import shutil
import pytesseract
from PIL import Image
from google import genai

class OCRProcessor:
    @staticmethod
    def extract_text(image_bytes):
        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            # --- ATTEMPT 1: Tesseract OCR (Best for Local Windows) ---
            tesseract_working = False
            if os.name == 'nt':
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                tesseract_working = os.path.exists(pytesseract.pytesseract.tesseract_cmd)
            else:
                tesseract_path = shutil.which("tesseract")
                if tesseract_path:
                    pytesseract.pytesseract.tesseract_cmd = tesseract_path
                    tesseract_working = True
            
            if tesseract_working:
                try:
                    text = pytesseract.image_to_string(image).strip()
                    if text:
                        return text
                except Exception as e:
                    print(f"Tesseract extraction failed: {e}")

            # --- ATTEMPT 2: Gemini Vision API (Fallback for Render Cloud) ---
            print("Tesseract unavailable or empty. Falling back to Gemini Vision OCR...")
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                print("Error: Gemini API Key missing for fallback OCR.")
                return ""
                
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=[
                    "You are a highly accurate OCR scanner. Extract all the text from this image exactly as it appears. Do not format the output. If there is absolutely no legible text, reply with exactly 'NO_TEXT_FOUND'.", 
                    image
                ]
            )
            
            extracted_text = response.text.strip()
            if "NO_TEXT_FOUND" in extracted_text:
                return ""
                
            return extracted_text

        except Exception as e:
            print(f"Fatal OCR Error: {e}")
            return ""