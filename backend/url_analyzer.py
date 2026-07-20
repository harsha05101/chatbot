from urllib.parse import urlparse
from knowledge_base import KNOWLEDGE_BASE

SUSPICIOUS_TLDS = {".xyz", ".top", ".club", ".online", ".site", ".info", ".biz", ".tk", ".ml"}

class URLAnalyzer:
    @staticmethod
    def analyze(url_str):
        if not url_str.startswith(("http://", "https://")):
            url_str = "http://" + url_str
            
        parsed = urlparse(url_str)
        domain = parsed.netloc.lower()
        
        score = 0
        reasons = []

        if not parsed.scheme == "https":
            score += 15
            reasons.append("Insecure HTTP protocol used")

        if any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS):
            score += 30
            reasons.append("Domain uses suspicious TLD extension")

        for key, info in KNOWLEDGE_BASE.items():
            if key in domain:
                if not any(domain.endswith(official) for official in info["official_domains"]):
                    score += 40
                    reasons.append(f"Impersonating brand {info['brand']} on fake domain")

        if domain.count(".") > 2:
            score += 15
            reasons.append("Excessive subdomains present")

        return {"domain": domain, "risk_score": score, "reasons": reasons}