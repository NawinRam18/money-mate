from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.transaction import Transaction
from app.models.merchant import Merchant
from app.api.auth import get_current_user


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.get("")
def get_transactions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: str | None = Query(None),
    payment_mode: str | None = Query(None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Transaction).filter(
        Transaction.user_id == user.id
    )

    if status:
        query = query.filter(
            Transaction.status == status.upper()
        )

    if payment_mode:
        query = query.filter(
            Transaction.payment_mode == payment_mode.upper()
        )

    total = query.count()

    offset = (page - 1) * limit

    transactions = query.order_by(
        Transaction.created_at.desc()
    ).offset(offset).limit(limit).all()

    data = []

    for transaction in transactions:
        merchant = db.query(Merchant).filter(
            Merchant.id == transaction.merchant_id
        ).first()

        data.append({
            "transaction_id": str(transaction.id),
            "merchant": merchant.name if merchant else None,
            "amount": str(transaction.amount),
            "currency": transaction.currency,
            "status": transaction.status,
            "risk_score": transaction.risk_score,
            "risk_level": transaction.risk_level,
            "risk_decision": transaction.risk_decision,
            "payment_mode": transaction.payment_mode,
            "created_at": transaction.created_at.isoformat()
        })

    total_pages = (total + limit - 1) // limit

    return {
        "success": True,
        "data": {
            "transactions": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": total_pages
            }
        },
        "error": None
    }


@router.get("/{transaction_id}")
def get_transaction(
    transaction_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not transaction_id or not transaction_id.strip():
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_TRANSACTION_ID",
                "message": "Transaction ID is required"
            }
        )

    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == user.id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TRANSACTION_NOT_FOUND",
                "message": "Transaction not found"
            }
        )

    merchant = db.query(Merchant).filter(
        Merchant.id == transaction.merchant_id
    ).first()

    return {
        "success": True,
        "data": {
            "transaction_id": str(transaction.id),
            "merchant": merchant.name if merchant else None,
            "amount": str(transaction.amount),
            "currency": transaction.currency,
            "status": transaction.status,
            "risk_score": transaction.risk_score,
            "risk_level": transaction.risk_level,
            "risk_decision": transaction.risk_decision,
            "risk_reasons": transaction.risk_reasons,
            "payment_mode": transaction.payment_mode,
            "is_offline": transaction.is_offline,
            "created_at": transaction.created_at.isoformat()
        },
        "error": None
    }