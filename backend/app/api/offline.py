from fastapi import APIRouter

from app.services.offline_verification import verify_transaction_hash

router = APIRouter()


@router.post("/offline/verify-hash")
def verify_offline_transaction(transaction: dict):
    is_valid = verify_transaction_hash(transaction)

    return {
        "valid": is_valid,
        "message": "Transaction hash is valid"
        if is_valid
        else "Transaction hash is invalid",
    }