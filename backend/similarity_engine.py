import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import TextPreprocessor

DATASETS = [
    {"category": "Banking Scam", "text": "Verify your SBI bank account immediately or account will be suspended KYC required."},
    {"category": "Delivery Scam", "text": "Your package delivery failed. Click link to update address and pay fee."},
    {"category": "UPI Scam", "text": "Paytm reward payment request! Enter UPI PIN to claim money in account."},
    {"category": "Lottery Scam", "text": "Congratulations you won $1,000,000 in lottery claim prize immediately."},
    {"category": "Job Scam", "text": "Part time online work earn $500 daily no experience required click to join whatsapp."}
]

class SimilarityEngine:
    def __init__(self):  # Added 'self' here
        self.df = pd.DataFrame(DATASETS)
        self.df['cleaned'] = self.df['text'].apply(TextPreprocessor.clean_text)
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['cleaned'])

    def find_match(self, input_text):
        cleaned = TextPreprocessor.clean_text(input_text)
        if not cleaned:
            return {"category": "Unknown", "similarity": 0.0}
            
        vec = self.vectorizer.transform([cleaned])
        sims = cosine_similarity(vec, self.tfidf_matrix)[0]
        
        max_idx = sims.argmax()
        max_sim = float(sims[max_idx])
        
        if max_sim > 0.15:
            return {
                "category": self.df.iloc[max_idx]["category"],
                "similarity": round(max_sim * 100, 2)
            }
        return {"category": "General Phishing", "similarity": 0.0}