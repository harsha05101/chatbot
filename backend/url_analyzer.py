# backend/url_analyzer.py
import re
from urllib.parse import urlparse

HIGH_RISK_TLDS = ['.xyz', '.top', '.club', '.online', '.site', '.info', '.tk', '.ml', '.ga', '.work', '.vip']
PROTECTED_BRANDS = ['paypal', 'google', 'apple', 'microsoft', 'amazon', 'netflix', 'wellsfargo', 'chase', 'bankofamerica', 'amrita']

class URLAnalyzer:
    @staticmethod
    def analyze(url: str) -> dict:
        reasons = []
        risk_score = 0
        
        # Ensure scheme for proper URL parsing
        formatted_url = url if url.startswith(('http://', 'https://')) else f'http://{url}'
        parsed = urlparse(formatted_url)
        domain = parsed.netloc.lower()
        
        # 1. Raw IP Address Check
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain):
            risk_score += 45
            reasons.append("Raw IP address used instead of a registered domain name.")

        # 2. High-Risk Disposable TLD Check
        if any(domain.endswith(tld) for tld in HIGH_RISK_TLDS):
            risk_score += 30
            reasons.append("Domain utilizes a high-risk TLD often associated with disposable phishing sites.")

        # 3. Brand Impersonation / Typosquatting Check
        for brand in PROTECTED_BRANDS:
            if brand in domain and not domain.endswith(f"{brand}.com") and not domain.endswith(f"{brand}.edu"):
                risk_score += 40
                reasons.append(f"Possible brand spoofing targeting '{brand}'.")
                break

        # 4. Excessive Subdomains Check
        if domain.count('.') > 3:
            risk_score += 25
            reasons.append("Excessive subdomain stacking detected to obscure actual destination.")

        # 5. Insecure Connection Check
        if url.startswith('http://'):
            risk_score += 15
            reasons.append("Insecure connection (HTTP) used instead of encrypted HTTPS.")

        return {
            "risk_score": min(risk_score, 100),
            "reasons": reasons if reasons else ["No suspicious URL indicators found."]
        }