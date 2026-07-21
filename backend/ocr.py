import os
import shutil
import pytesseract
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Ensure API keys are loaded specifically for this file
load_dotenv()

class OCRProcessor:
    @staticmethod
    def extract_text(image_bytes):
        try:
            # --- ATTEMPT 1: Tesseract OCR (Local) ---
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
                    from PIL import Image
                    import io
                    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                    text = pytesseract.image_to_string(image).strip()
                    if text:
                        print(f"✅ Tesseract Success! Extracted {len(text)} characters.")
                        return text
                    else:
                        print("⚠️ Tesseract ran but found no text. Falling back to Gemini...")
                except Exception as e:
                    print(f"⚠️ Tesseract error: {e}")
            else:
                print("⚠️ Tesseract unavailable. Falling back to Gemini...")

            # --- ATTEMPT 2: Gemini Vision API (Render Cloud Fallback) ---
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                print("❌ Error: GEMINI_API_KEY missing in environment variables!")
                return ""
                
            print("🚀 Sending image bytes directly to Gemini Vision API...")
            client = genai.Client(api_key=api_key)
            
            # Use the strict Part.from_bytes syntax required by the new SDK
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
                    "Extract all text from this image exactly as it appears. If there is absolutely no legible text, reply with exactly 'NO_TEXT_FOUND'."
                ]
            )
            
            extracted_text = response.text.strip()
            if "NO_TEXT_FOUND" in extracted_text or not extracted_text:
                print("❌ Gemini Vision returned NO_TEXT_FOUND.")
                return ""
                
            print(f"✅ Gemini Success! Extracted {len(extracted_text)} characters.")
            return extracted_text

        except Exception as e:
            print(f"❌ Fatal OCR Error: {e}")
            return ""