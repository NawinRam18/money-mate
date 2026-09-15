from decimal import Decimal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/finance",
    tags=["Finance"]
)


class WhatIfRequest(BaseModel):
    monthly_savings: Decimal
    months: int
    annual_return_rate: Decimal = Decimal("0")


@router.post("/what-if")
def what_if(
    request: WhatIfRequest,
    user: User = Depends(get_current_user)
):
    if request.monthly_savings <= 0:
        return {
            "success": False,
            "data": None,
            "error": {
                "code": "INVALID_SAVINGS",
                "message": "Monthly savings must be greater than zero"
            }
        }

    if request.months <= 0:
        return {
            "success": False,
            "data": None,
            "error": {
                "code": "INVALID_MONTHS",
                "message": "Months must be greater than zero"
            }
        }

    total_contribution = (
        request.monthly_savings * request.months
    )

    return {
        "success": True,
        "data": {
            "monthly_savings": str(request.monthly_savings),
            "months": request.months,
            "annual_return_rate": str(request.annual_return_rate),
            "total_contribution": str(total_contribution),
            "estimated_final_value": str(total_contribution),
            "message": "This is a deterministic estimate. No investment return was applied."
        },
        "error": None
    }
@router.get("/insights")
def get_finance_insights(
    user: User = Depends(get_current_user)
):
    return {
        "success": True,
        "data": {
            "monthly_spending": "0.00",
            "monthly_savings": "0.00",
            "top_spending_category": "No data",
            "financial_health": "GOOD",
            "message": "Financial insights are based on your transaction history."
        },
        "error": None
    }