from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import app
from app.db.session import SessionLocal
from app.models.user import User
from app.models.wallet import Wallet


client = TestClient(app)


def get_token():
    response = client.post(
        "/api/v1/auth/login",
        params={
            "email": "test_user_12345@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 200

    return response.json()["data"]["access_token"]


def create_test_wallet():
    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.email == "test_user_12345@example.com"
        ).first()

        assert user is not None

        wallet = db.query(Wallet).filter(
            Wallet.user_id == user.id
        ).first()

        if not wallet:
            wallet = Wallet(
                user_id=user.id,
                currency="INR",
                balance=Decimal("10000.00"),
                available_balance=Decimal("10000.00")
            )

            db.add(wallet)
            db.commit()

    finally:
        db.close()


def test_payment_idempotency():
    create_test_wallet()

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Idempotency-Key": "PYTEST-PAYMENT-001"
    }

    response1 = client.post(
        "/api/v1/payments",
        params={
            "amount": "100",
            "merchant_identifier": "AMAZON001"
        },
        headers=headers
    )

    assert response1.status_code == 200, response1.text

    data1 = response1.json()

    assert data1["success"] is True
    assert "transaction_id" in data1["data"]

    transaction_id = data1["data"]["transaction_id"]

    response2 = client.post(
        "/api/v1/payments",
        params={
            "amount": "100",
            "merchant_identifier": "AMAZON001"
        },
        headers=headers
    )

    assert response2.status_code == 200, response2.text

    data2 = response2.json()

    assert data2["success"] is True
    assert data2["data"]["transaction_id"] == transaction_id
    assert "No duplicate charge" in data2["data"]["message"]