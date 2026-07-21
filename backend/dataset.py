# backend/dataset.py

SCAM_DATASET = [
    {
        "text": "Alert: Your bank account has been suspended due to unauthorized login attempts. Verify your details immediately to restore access: http://secure-bank-login.com",
        "category": "Banking Fraud",
        "risk_score": 95
    },
    {
        "text": "Your card was used for $499.99 at Target. If this was not you, call support immediately or click here to decline.",
        "category": "Financial Fraud",
        "risk_score": 90
    },
    {
        "text": "Your debit card is blocked. Unblock now by providing your PIN and OTP at http://update-card-details.net",
        "category": "Banking Fraud",
        "risk_score": 95
    },
    {
        "text": "Your password for Google Workspace will expire today. Click here to maintain your current password.",
        "category": "Credential Harvesting",
        "risk_score": 92
    },
    {
        "text": "IT Desk: Scheduled maintenance required. Please re-enter your corporate SSO login credentials to prevent account lockout.",
        "category": "Corporate Impersonation",
        "risk_score": 88
    },
    {
        "text": "Security Alert: Someone attempted to sign into your account from an unrecognized device. Review activity at http://g-account-verify.org",
        "category": "Account Impersonation",
        "risk_score": 88
    },
    {
        "text": "USPS: Package delivery failure due to unpaid customs fee of $1.50. Update delivery address and pay fee here.",
        "category": "Delivery Scam",
        "risk_score": 85
    },
    {
        "text": "FedEx: Your package is on hold at our local hub. Confirm your delivery preferences within 24 hours at http://fedex-redelivery-track.com",
        "category": "Delivery Scam",
        "risk_score": 85
    },
    {
        "text": "Earn $300-$800 daily working 1 hour from home. No experience needed. Contact our recruiter on WhatsApp immediately.",
        "category": "Job Scam",
        "risk_score": 80
    },
    {
        "text": "Your OTP for login is 492018. It is valid for 10 minutes. Do not share this code with anyone.",
        "category": "Legitimate OTP",
        "risk_score": 0
    },
    {
        "text": "Hi, are we still meeting for lunch at 1 PM today?",
        "category": "Legitimate Message",
        "risk_score": 0
    }
]