from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.wallet import Wallet
from app.api.auth import get_current_user


router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"]
)


@router.get("")
def get_wallet(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
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

    return {
        "success": True,
        "data": {
            "wallet_id": str(wallet.id),
            "user_id": str(wallet.user_id),
            "currency": wallet.currency,
            "balance": str(wallet.balance),
            "available_balance": str(wallet.available_balance)
        },
        "error": None
    }