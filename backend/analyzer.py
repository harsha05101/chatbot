import os
import json
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Create Gemini client
client = genai.Client(api_key=api_key)


def analyze_phishing(text):
    prompt = f"""
You are an expert cybersecurity analyst.

Analyze the following email, SMS, URL, or message for phishing.

Return ONLY valid JSON in the following format:

{{
  "risk": "High/Medium/Low",
  "confidence": "95%",
  "reasons": [
    "...",
    "..."
  ],
  "recommendation": [
    "...",
    "..."
  ]
}}

Message:
{text}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    result = response.text.strip()

    # Remove markdown if Gemini returns ```json ... ```
    if result.startswith("```json"):
        result = result.replace("```json", "").replace("```", "").strip()
    elif result.startswith("```"):
        result = result.replace("```", "").strip()

    try:
        return json.loads(result)
    except Exception:
        return {
            "risk": "Unknown",
            "confidence": "0%",
            "reasons": [result],
            "recommendation": [
                "Gemini returned a response that was not valid JSON."
            ]
        }