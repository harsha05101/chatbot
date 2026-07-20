class RuleEngine:
    @staticmethod
    def evaluate(features, entities, url_risk_score=0):
        score = 0
        reasons = []

        if len(entities.get("urls", [])) > 0:
            score += 20
            reasons.append("Contains suspicious link(s)")
            
        if url_risk_score > 50:
            score += 25
            reasons.append("High-risk domain structure detected")

        if features.get("urgent_words", 0) > 0:
            score += 15
            reasons.append("Creates high sense of urgency")

        if features.get("bank_words", 0) > 0:
            score += 10
            reasons.append("Mentions banking/KYC terms")

        if features.get("reward_words", 0) > 0:
            score += 20
            reasons.append("Promises prizes or monetary reward")

        if features.get("caps_ratio", 0) > 0.3:
            score += 10
            reasons.append("Excessive use of UPPERCASE letters")

        final_score = min(score, 100)
        
        if final_score <= 30:
            risk_level = "Low"
        elif final_score <= 60:
            risk_level = "Medium"
        else:
            risk_level = "High"

        return {
            "score": final_score,
            "level": risk_level,
            "reasons": reasons
        }