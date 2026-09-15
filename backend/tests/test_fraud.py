from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import app
from app.db.session import SessionLocal
from app.models.user import User
from app.models.wallet import Wallet


client = TestClient(app)


TEST_EMAIL = "test_user_12345@example.com"
TEST_PASSWORD = "TestPassword123"


def get_token():
    response = client.post(
        "/api/v1/auth/login",
        params={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
    )

    assert response.status_code == 200, response.text

    return response.json()["data"]["access_token"]


def get_wallet():
    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.email == TEST_EMAIL
        ).first()

        assert user is not None

        wallet = db.query(Wallet).filter(
            Wallet.user_id == user.id
        ).first()

        assert wallet is not None

        return wallet

    finally:
        db.close()


def test_critical_payment_is_blocked():
    token = get_token()

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.email == TEST_EMAIL
        ).first()

        assert user is not None

        wallet = db.query(Wallet).filter(
            Wallet.user_id == user.id
        ).first()

        assert wallet is not None

        original_balance = Decimal(str(wallet.balance))

        wallet.balance = Decimal("50000.00")
        wallet.available_balance = Decimal("50000.00")

        db.commit()

    finally:
        db.close()

    headers = {
        "Authorization": f"Bearer {token}",
        "Idempotency-Key": "PYTEST-FRAUD-BLOCK-002"
    }

    response = client.post(
        "/api/v1/payments",
        params={
            "amount": "25000",
            "merchant_identifier": "UNKNOWN001"
        },
        headers=headers
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["success"] is True
    assert data["data"]["status"] == "BLOCKED"

    wallet = get_wallet()

    assert Decimal(str(wallet.balance)) == Decimal("50000.00")

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.email == TEST_EMAIL
        ).first()

        wallet = db.query(Wallet).filter(
            Wallet.user_id == user.id
        ).first()

        wallet.balance = original_balance
        wallet.available_balance = original_balance

        db.commit()

    finally:
        db.close()