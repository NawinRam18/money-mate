from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.auth import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"]
)


class AIChatRequest(BaseModel):
    message: str


@router.post("/chat")
def ai_chat(
    request: AIChatRequest,
    user: User = Depends(get_current_user)
):
    message = request.message.lower()

    if "balance" in message:
        response = (
            "You can check your current wallet balance "
            "using the MONEY-MATE wallet section."
        )

    elif "save" in message:
        response = (
            "You can use the Finance What-If calculator "
            "to estimate how much you could save over time."
        )

    elif "fraud" in message or "suspicious" in message:
        response = (
            "MONEY-MATE uses fraud risk evaluation to identify "
            "suspicious transactions before payment authorization."
        )

    elif "mandate" in message or "subscription" in message:
        response = (
            "You can view and manage your recurring payment "
            "mandates through the Mandates section."
        )

    else:
        response = (
            "I can help with wallet balance, savings, "
            "fraud protection, subscriptions, and payments."
        )

    return {
        "success": True,
        "data": {
            "message": request.message,
            "response": response,
            "assistant_type": "demo",
            "payment_authorization": False
        },
        "error": None
    }