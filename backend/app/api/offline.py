from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.wallet import Wallet
from app.models.offline_transaction import OfflineTransaction
from app.models.security_event import SecurityEvent
from app.services.offline_service import verify_hash
from app.services.offline_verification import verify_transaction_hash


router = APIRouter()


class OfflineTransactionRequest(BaseModel):
    offline_transaction_id: str
    counter: int
    timestamp: str
    recipient_identifier: str
    amount: str
    previous_hash: str
    current_hash: str


@router.post("/offline/verify-hash")
def verify_offline_transaction(transaction: dict):
    is_valid = verify_transaction_hash(transaction)

    return {
        "valid": is_valid,
        "message": "Transaction hash is valid"
        if is_valid
        else "Transaction hash is invalid",
    }


@router.post("/offline/sync")
def sync_offline_transaction(
    request: OfflineTransactionRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(OfflineTransaction).filter(
        OfflineTransaction.offline_transaction_id
        == request.offline_transaction_id
    ).first()

    if existing:
        security_event = SecurityEvent(
            user_id=user.id,
            event_type="OFFLINE_REPLAY",
            severity="MEDIUM",
            description="Duplicate offline transaction submission detected"
        )

        db.add(security_event)
        db.commit()

        return {
            "success": True,
            "data": {
                "offline_transaction_id":
                    existing.offline_transaction_id,
                "status": existing.status,
                "message": "Offline transaction already synced"
            },
            "error": None
        }

    transaction_data = {
        "offline_transaction_id":
            request.offline_transaction_id,
        "counter": request.counter,
        "timestamp": request.timestamp,
        "recipient_identifier":
            request.recipient_identifier,
        "amount": request.amount
    }

    is_valid = verify_hash(
        transaction_data,
        request.previous_hash,
        request.current_hash
    )

    if not is_valid:
        security_event = SecurityEvent(
            user_id=user.id,
            event_type="OFFLINE_TAMPERING",
            severity="HIGH",
            description="Offline transaction hash verification failed"
        )

        db.add(security_event)
        db.commit()

        return {
            "success": False,
            "data": {
                "offline_transaction_id":
                    request.offline_transaction_id,
                "status": "REJECTED",
                "reason": "Hash verification failed"
            },
            "error": {
                "code": "HASH_MISMATCH",
                "message":
                    "Offline transaction failed integrity verification"
            }
        }

    wallet = db.query(Wallet).filter(
        Wallet.user_id == user.id
    ).first()

    if not wallet:
        return {
            "success": False,
            "data": None,
            "error": {
                "code": "WALLET_NOT_FOUND",
                "message": "Wallet not found"
            }
        }

    offline_transaction = OfflineTransaction(
        user_id=user.id,
        wallet_id=wallet.id,
        offline_transaction_id=
            request.offline_transaction_id,
        counter=request.counter,
        timestamp=request.timestamp,
        recipient_identifier=
            request.recipient_identifier,
        amount=request.amount,
        previous_hash=request.previous_hash,
        current_hash=request.current_hash,
        signature="DEMO_SIGNATURE",
        status="SYNCED"
    )

    db.add(offline_transaction)
    db.commit()
    db.refresh(offline_transaction)

    return {
        "success": True,
        "data": {
            "offline_transaction_id":
                offline_transaction.offline_transaction_id,
            "status": offline_transaction.status,
            "amount": str(offline_transaction.amount),
            "recipient_identifier":
                offline_transaction.recipient_identifier,
            "message":
                "Offline transaction verified and synced successfully"
        },
        "error": None
    }