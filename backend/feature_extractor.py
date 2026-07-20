import re

URGENT_WORDS = {"urgent", "immediately", "verify", "suspend", "action", "required", "blocked", "locked", "expire", "alert"}
BANK_WORDS = {"sbi", "hdfc", "icici", "bank", "account", "kyc", "netbanking", "atm", "card", "pin", "otp"}
REWARD_WORDS = {"winner", "congratulations", "won", "prize", "lottery", "claim", "reward", "cash", "free", "gift"}

class FeatureExtractor:
    @staticmethod
    def extract(text):
        if not text:
            return {}
        
        words = re.findall(r'\w+', text.lower())
        total_words = len(words) or 1
        
        caps_count = sum(1 for c in text if c.isupper())
        special_count = sum(1 for c in text if c in "!@#$%^&*()_+-=[]{}|;:'\",.<>/?")
        
        urgent_count = sum(1 for w in words if w in URGENT_WORDS)
        bank_count = sum(1 for w in words if w in BANK_WORDS)
        reward_count = sum(1 for w in words if w in REWARD_WORDS)
        
        return {
            "urgent_words": urgent_count,
            "bank_words": bank_count,
            "reward_words": reward_count,
            "caps_ratio": round(caps_count / max(len(text), 1), 2),
            "special_char_count": special_count,
            "message_length": len(text),
            "word_count": total_words
        }