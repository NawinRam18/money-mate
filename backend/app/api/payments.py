from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.wallet import Wallet
from app.models.merchant import Merchant
from app.models.transaction import Transaction
from app.api.auth import get_current_user
from app.services.fraud_service import evaluate_payment
from app.services.audit_service import create_audit_log


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


def validate_amount(amount: Decimal):
    if amount <= 0:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_AMOUNT",
                "message": "Payment amount must be greater than zero"
            }
        )

    if amount.as_tuple().exponent < -2:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_AMOUNT",
                "message": "Payment amount cannot have more than 2 decimal places"
            }
        )


def validate_merchant_identifier(merchant_identifier: str):
    if not merchant_identifier or not merchant_identifier.strip():
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_MERCHANT",
                "message": "Merchant identifier is required"
            }
        )


def validate_idempotency_key(idempotency_key: str):
    if not idempotency_key or not idempotency_key.strip():
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_IDEMPOTENCY_KEY",
                "message": "Idempotency-Key cannot be empty"
            }
        )

    if len(idempotency_key) > 255:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_IDEMPOTENCY_KEY",
                "message": "Idempotency-Key must not exceed 255 characters"
            }
        )


@router.post("")
def create_payment(
    amount: Decimal,
    merchant_identifier: str,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    validate_amount(amount)
    validate_merchant_identifier(merchant_identifier)
    validate_idempotency_key(idempotency_key)

    merchant_identifier = merchant_identifier.strip()
    idempotency_key = idempotency_key.strip()

    existing_transaction = db.query(Transaction).filter(
        Transaction.user_id == user.id,
        Transaction.idempotency_key == idempotency_key
    ).first()

    if existing_transaction:
        merchant = db.query(Merchant).filter(
            Merchant.id == existing_transaction.merchant_id
        ).first()

        return {
            "success": True,
            "data": {
                "transaction_id": str(existing_transaction.id),
                "merchant": merchant.name if merchant else None,
                "amount": str(existing_transaction.amount),
                "currency": existing_transaction.currency,
                "status": existing_transaction.status,
                "risk_score": existing_transaction.risk_score,
                "risk_level": existing_transaction.risk_level,
                "risk_decision": existing_transaction.risk_decision,
                "risk_reasons": existing_transaction.risk_reasons,
                "message": "Existing payment returned. No duplicate charge."
            },
            "error": None
        }

    wallet = db.query(Wallet).filter(
        Wallet.user_id == user.id
    ).with_for_update().first()

    if not wallet:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "WALLET_NOT_FOUND",
                "message": "Wallet not found"
            }
        )

    if wallet.available_balance < amount:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INSUFFICIENT_BALANCE",
                "message": "Insufficient wallet balance"
            }
        )

    merchant = db.query(Merchant).filter(
        Merchant.identifier == merchant_identifier
    ).first()

    if not merchant:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "MERCHANT_NOT_FOUND",
                "message": "Merchant not found"
            }
        )

    fraud_result = evaluate_payment(
        amount=amount,
        merchant_risk_level=merchant.risk_level,
        merchant_verified=merchant.is_verified
    )

    if fraud_result["risk_decision"] == "BLOCK":
        create_audit_log(
            db=db,
            user_id=user.id,
            action="PAYMENT_BLOCKED",
            resource_type="PAYMENT",
            description="Payment blocked by fraud detection",
            details={
                "amount": str(amount),
                "merchant": merchant.name,
                "risk_score": fraud_result["risk_score"],
                "risk_level": fraud_result["risk_level"],
                "risk_reasons": fraud_result["risk_reasons"]
            }
        )

        db.commit()

        return {
            "success": False,
            "data": {
                "risk_score": fraud_result["risk_score"],
                "risk_level": fraud_result["risk_level"],
                "risk_decision": fraud_result["risk_decision"],
                "risk_reasons": fraud_result["risk_reasons"]
            },
            "error": {
                "code": "PAYMENT_BLOCKED",
                "message": "Payment blocked by fraud detection"
            }
        }

    if fraud_result["risk_decision"] in ["WARN", "STEP_UP"]:
        transaction = Transaction(
            user_id=user.id,
            wallet_id=wallet.id,
            merchant_id=merchant.id,
            amount=amount,
            currency="INR",
            status="PENDING",
            risk_score=fraud_result["risk_score"],
            risk_level=fraud_result["risk_level"],
            risk_decision=fraud_result["risk_decision"],
            risk_reasons=fraud_result["risk_reasons"],
            payment_mode="ONLINE",
            is_offline=False,
            idempotency_key=idempotency_key
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return {
            "success": True,
            "data": {
                "transaction_id": str(transaction.id),
                "merchant": merchant.name,
                "amount": str(amount),
                "currency": "INR",
                "status": transaction.status,
                "risk_score": fraud_result["risk_score"],
                "risk_level": fraud_result["risk_level"],
                "risk_decision": fraud_result["risk_decision"],
                "risk_reasons": fraud_result["risk_reasons"],
                "message": "Payment requires confirmation"
            },
            "error": None
        }

    transaction = Transaction(
        user_id=user.id,
        wallet_id=wallet.id,
        merchant_id=merchant.id,
        amount=amount,
        currency="INR",
        status="COMPLETED",
        risk_score=fraud_result["risk_score"],
        risk_level=fraud_result["risk_level"],
        risk_decision=fraud_result["risk_decision"],
        risk_reasons=fraud_result["risk_reasons"],
        payment_mode="ONLINE",
        is_offline=False,
        idempotency_key=idempotency_key
    )

    wallet.balance -= amount
    wallet.available_balance -= amount

    db.add(transaction)

    create_audit_log(
        db=db,
        user_id=user.id,
        action="PAYMENT_COMPLETED",
        resource_type="PAYMENT",
        resource_id=str(transaction.id),
        description="Payment completed successfully",
        details={
            "amount": str(amount),
            "merchant": merchant.name,
            "risk_score": fraud_result["risk_score"],
            "risk_level": fraud_result["risk_level"],
            "risk_decision": fraud_result["risk_decision"]
        }
    )

    db.commit()
    db.refresh(transaction)

    return {
        "success": True,
        "data": {
            "transaction_id": str(transaction.id),
            "merchant": merchant.name,
            "amount": str(amount),
            "currency": "INR",
            "status": transaction.status,
            "risk_score": transaction.risk_score,
            "risk_level": transaction.risk_level,
            "risk_decision": transaction.risk_decision,
            "risk_reasons": transaction.risk_reasons,
            "remaining_balance": str(wallet.balance)
        },
        "error": None
    }


@router.post("/{transaction_id}/confirm")
def confirm_payment(
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

    if transaction.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_TRANSACTION_STATUS",
                "message": "Only pending payments can be confirmed"
            }
        )

    wallet = db.query(Wallet).filter(
        Wallet.id == transaction.wallet_id,
        Wallet.user_id == user.id
    ).with_for_update().first()

    if not wallet:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "WALLET_NOT_FOUND",
                "message": "Wallet not found"
            }
        )

    if wallet.available_balance < transaction.amount:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INSUFFICIENT_BALANCE",
                "message": "Insufficient wallet balance"
            }
        )

    wallet.balance -= transaction.amount
    wallet.available_balance -= transaction.amount

    transaction.status = "COMPLETED"

    create_audit_log(
        db=db,
        user_id=user.id,
        action="PAYMENT_CONFIRMED",
        resource_type="PAYMENT",
        resource_id=str(transaction.id),
        description="Pending payment confirmed successfully",
        details={
            "amount": str(transaction.amount),
            "risk_level": transaction.risk_level,
            "risk_decision": transaction.risk_decision
        }
    )

    db.commit()
    db.refresh(transaction)

    return {
        "success": True,
        "data": {
            "transaction_id": str(transaction.id),
            "amount": str(transaction.amount),
            "currency": transaction.currency,
            "status": transaction.status,
            "risk_level": transaction.risk_level,
            "risk_decision": transaction.risk_decision,
            "message": "Payment confirmed successfully",
            "remaining_balance": str(wallet.balance)
        },
        "error": None
    }