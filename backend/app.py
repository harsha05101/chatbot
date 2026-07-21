# backend/app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

from preprocess import TextPreprocessor
from feature_extractor import FeatureExtractor
from rule_engine import RuleEngine
from similarity_engine import SimilarityEngine
from url_analyzer import URLAnalyzer
from ocr import OCRProcessor
from database import init_db, save_scan

# Initialize Flask App
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Database & Engine
init_db()
similarity_engine = SimilarityEngine()

# Initialize Gemini Client cleanly from environment variable
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


@app.route('/', methods=['GET'])
def home():
    return "PhishGuard AI Backend Running Successfully!"


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        image_bytes = file.read()
        extracted_text = OCRProcessor.extract_text(image_bytes)

        return jsonify({'extracted_text': extracted_text})
    except Exception as e:
        print(f"Upload Endpoint Error: {e}")
        return jsonify({'error': 'Failed to process image'}), 500


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

    # 1. Pipeline Execution
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

    # 4. Gemini Deep AI Threat Intelligence Analysis
    try:
        if not client:
            raise ValueError("GEMINI_API_KEY environment variable not set.")

        prompt = f"""
        You are PhishGuard AI, an elite cybersecurity threat intelligence analyst. 

        Analyze the message below and synthesize the technical pipeline findings into a clear, professional security assessment.

        --- CONTENT FOR ANALYSIS ---
        "{text}"

        --- PIPELINE THREAT METRICS ---
        Calculated Risk: {rule_res['score']}/100 ({rule_res['level']} Risk)
        Matched Category: {match_res['category']}
        Detected Anomalies: {', '.join(combined_reasons) if combined_reasons else 'None'}

        --- RESPONSE FORMAT INSTRUCTIONS ---
        Provide your assessment formatted EXACTLY as follows (no codeblock formatting, keep it clean):

        🔍 **Threat Breakdown**: (In 2 concise sentences, state the tactic being used—e.g., social engineering, urgent action bias, brand impersonation, or fake credential check).

        ⚠️ **Key Red Flags**:
        • [Flag 1: Specific suspicious keyword, link pattern, or urgency tactic found in the content]
        • [Flag 2: Another notable anomaly or lack of standard security practices]

        🛡️ **Recommended Actions**:
        1. [Action 1: Immediate step for the user]
        2. [Action 2: Preventive step to protect their identity or account]
        """

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        gemini_response = response.text.strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        gemini_response = (
            "🔍 **Threat Breakdown**: Evaluated using rule-based pattern matching and heuristic detection.\n\n"
            "⚠️ **Key Red Flags**:\n"
            "• High-risk language or unverified URL structures detected.\n"
            "• Unwanted solicitation or urgency prompt.\n\n"
            "🛡️ **Recommended Actions**:\n"
            "1. Do not click any links or provide personal credentials.\n"
            "2. Verify through the official institution portal directly."
        )

    # 5. Save Scan History
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


if __name__ == "__main__":
    app.run(port=5000, debug=True)