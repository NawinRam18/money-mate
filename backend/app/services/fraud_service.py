from decimal import Decimal


def evaluate_payment(
    amount: Decimal,
    merchant_risk_level: str,
    merchant_verified: bool
):
    risk_score = 0
    reasons = []

    if amount >= Decimal("20000"):
        risk_score += 50
        reasons.append("High transaction amount")
    elif amount >= Decimal("10000"):
        risk_score += 30
        reasons.append("Unusually large transaction")

    if merchant_risk_level == "HIGH":
        risk_score += 30
        reasons.append("High-risk merchant")

    if not merchant_verified:
        risk_score += 20
        reasons.append("Unverified merchant")

    if risk_score <= 30:
        risk_level = "LOW"
        decision = "APPROVE"
    elif risk_score <= 60:
        risk_level = "MEDIUM"
        decision = "WARN"
    elif risk_score <= 80:
        risk_level = "HIGH"
        decision = "STEP_UP"
    else:
        risk_level = "CRITICAL"
        decision = "BLOCK"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_decision": decision,
        "risk_reasons": reasons,
        "model_source": "fallback"
    }