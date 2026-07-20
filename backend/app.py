from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os

from preprocess import TextPreprocessor
from feature_extractor import FeatureExtractor
from rule_engine import RuleEngine
from similarity_engine import SimilarityEngine
from url_analyzer import URLAnalyzer
from ocr import OCRProcessor
from database import init_db, save_scan

app = Flask(__name__)
CORS(app)

# Initialize Database & Engine
init_db()
similarity_engine = SimilarityEngine()

# Initialize Gemini Client
api_key = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_KEY")
client = genai.Client(api_key=api_key)


@app.route('/', methods=['GET'])
def home():
    return "PhishGuard AI Backend Running Successfully!"


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("message", "") or data.get("text", "")

    if not text.strip():
        return jsonify({
            "risk_score": 0,
            "risk_level": "Low",
            "category": "None",
            "similarity": 0,
            "reasons": ["No content provided for analysis."],
            "explanation": "Please enter a valid message, email, or URL to analyze."
        })

    # 1. NLP Pipeline Execution
    entities = TextPreprocessor.extract_entities(text)
    features = FeatureExtractor.extract(text)

    # 2. URL & Link Analysis
    url_risk = 0
    url_reasons = []
    if entities.get("urls"):
        url_res = URLAnalyzer.analyze(entities["urls"][0])
        url_risk = url_res["risk_score"]
        url_reasons = url_res["reasons"]

    # 3. Rule Engine & Similarity Matching
    rule_res = RuleEngine.evaluate(features, entities, url_risk)
    match_res = similarity_engine.find_match(text)
    combined_reasons = rule_res["reasons"] + url_reasons

    # 4. Gemini Deep AI Analysis & Response Generation
    try:
        prompt = f"""
        You are PhishGuard AI, a top cybersecurity analyst. Analyze the following content and the rule engine findings to provide a concise, user-friendly security assessment.

        --- PIPELINE FINDINGS ---
        Content Analyzed: "{text}"
        Calculated Risk Score: {rule_res['score']}/100 ({rule_res['level']} Risk)
        Scam Category Match: {match_res['category']}
        Detected Risk Factors: {', '.join(combined_reasons) if combined_reasons else 'None'}
        Extracted Entities: URLs: {entities.get('urls', [])}, Emails: {entities.get('emails', [])}, Phone Numbers: {entities.get('phones', [])}

        --- INSTRUCTIONS ---
        1. Explain WHY this message is safe or dangerous in 2 short bullet points based on indicators (urgency, domain legitimacy, reward traps, impersonation).
        2. Provide 2 clear, practical action steps for the user to stay safe.
        3. Keep the tone helpful, professional, and clear. Do not wrap in markdown codeblocks.
        """

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        gemini_response = response.text.strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        gemini_response = (
            "• This message was evaluated using rule-based pattern detection.\n"
            "• Exercise caution if it requests sensitive personal details, passwords, or immediate payments."
        )

    # 5. Save History
    save_scan(text, rule_res['score'], match_res['category'], match_res['similarity'])

    return jsonify({
        "risk_score": rule_res['score'],
        "risk_level": rule_res['level'],
        "category": match_res['category'],
        "similarity": match_res['similarity'],
        "reasons": combined_reasons,
        "explanation": gemini_response,
        "features": features
    })


@app.route('/upload', methods=['POST'])
def upload_ocr():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    text = OCRProcessor.extract_text(file.read())
    return jsonify({"extracted_text": text})


if __name__ == "__main__":
    app.run(port=5000, debug=True)