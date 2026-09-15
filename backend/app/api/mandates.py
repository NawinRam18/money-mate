from decimal import Decimal
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.mandate import Mandate
from app.api.auth import get_current_user


router = APIRouter(
    prefix="/mandates",
    tags=["Mandates"]
)


class MandateCreateRequest(BaseModel):
    merchant_name: str
    merchant_identifier: str
    amount: Decimal
    frequency: str
    next_payment_date: date


@router.post("")
def create_mandate(
    request: MandateCreateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if request.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Mandate amount must be greater than zero"
        )

    mandate = Mandate(
        user_id=user.id,
        merchant_name=request.merchant_name,
        merchant_identifier=request.merchant_identifier,
        amount=request.amount,
        frequency=request.frequency,
        next_payment_date=request.next_payment_date,
        status="ACTIVE"
    )

    db.add(mandate)
    db.commit()
    db.refresh(mandate)

    return {
        "success": True,
        "data": {
            "mandate_id": str(mandate.id),
            "merchant_name": mandate.merchant_name,
            "amount": str(mandate.amount),
            "frequency": mandate.frequency,
            "next_payment_date": str(mandate.next_payment_date),
            "status": mandate.status
        },
        "error": None
    }


@router.get("")
def get_mandates(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mandates = db.query(Mandate).filter(
        Mandate.user_id == user.id
    ).all()

    data = []

    for mandate in mandates:
        data.append({
            "mandate_id": str(mandate.id),
            "merchant_name": mandate.merchant_name,
            "merchant_identifier": mandate.merchant_identifier,
            "amount": str(mandate.amount),
            "frequency": mandate.frequency,
            "next_payment_date": str(mandate.next_payment_date),
            "status": mandate.status
        })

    return {
        "success": True,
        "data": data,
        "error": None
    }