print("FRAUD FILE LOADED")
from decimal import Decimal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.merchant import Merchant
from app.api.auth import get_current_user
from app.services.fraud_service import evaluate_payment


router = APIRouter(
    prefix="/fraud",
    tags=["Fraud Detection"]
)


class FraudEvaluationRequest(BaseModel):
    amount: Decimal
    merchant_identifier: str


@router.post("/evaluate")
def evaluate_fraud(
    request: FraudEvaluationRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    merchant = db.query(Merchant).filter(
        Merchant.identifier == request.merchant_identifier
    ).first()

    if not merchant:
        return {
            "success": False,
            "data": None,
            "error": {
                "code": "MERCHANT_NOT_FOUND",
                "message": "Merchant not found"
            }
        }

    if request.amount <= 0:
        return {
            "success": False,
            "data": None,
            "error": {
                "code": "INVALID_AMOUNT",
                "message": "Amount must be greater than zero"
            }
        }

    result = evaluate_payment(
        amount=request.amount,
        merchant_risk_level=merchant.risk_level,
        merchant_verified=merchant.is_verified
    )

    return {
        "success": True,
        "data": {
            "merchant": merchant.name,
            "amount": str(request.amount),
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "risk_decision": result["risk_decision"],
            "risk_reasons": result["risk_reasons"],
            "model_source": result["model_source"]
        },
        "error": None
    }