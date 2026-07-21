import os
import io
from PIL import Image
from google import genai

class OCRProcessor:
    @staticmethod
    def extract_text(image_bytes):
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                print("Error: Gemini API Key not found for OCR.")
                return ""

            # Initialize Gemini Client
            client = genai.Client(api_key=api_key)
            
            # Load the image using Pillow
            image = Image.open(io.BytesIO(image_bytes))

            # Prompt Gemini to extract the text
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=[
                    "You are an OCR engine. Extract all the text from this image exactly as it appears. If there is no legible text, reply with exactly 'NO_TEXT_FOUND'.", 
                    image
                ]
            )
            
            extracted_text = response.text.strip()
            
            if "NO_TEXT_FOUND" in extracted_text:
                return ""
                
            return extracted_text
            
        except Exception as e:
            print(f"Vision OCR Error: {e}")
            return ""