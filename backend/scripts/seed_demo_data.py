from decimal import Decimal

from app.db.session import SessionLocal
from app.models.user import User
from app.models.wallet import Wallet
from app.models.merchant import Merchant


db = SessionLocal()

try:
    user = db.query(User).filter(
        User.email == "test@moneymate.com"
    ).first()

    if not user:
        print("Demo user not found")
    else:
        wallet = db.query(Wallet).filter(
            Wallet.user_id == user.id
        ).first()

        if wallet:
            print("Wallet already exists")
        else:
            wallet = Wallet(
                user_id=user.id,
                currency="INR",
                balance=Decimal("75000.00"),
                available_balance=Decimal("75000.00")
            )

            db.add(wallet)
            db.commit()

            print("Demo wallet created successfully")
            print("Balance: ₹75000.00")

        merchants = [
            {
                "name": "Amazon",
                "category": "Shopping",
                "identifier": "AMAZON001",
                "risk_level": "LOW",
                "is_verified": True
            },
            {
                "name": "Swiggy",
                "category": "Food Delivery",
                "identifier": "SWIGGY001",
                "risk_level": "LOW",
                "is_verified": True
            },
            {
                "name": "Zomato",
                "category": "Food Delivery",
                "identifier": "ZOMATO001",
                "risk_level": "LOW",
                "is_verified": True
            },
            {
                "name": "Netflix",
                "category": "Entertainment",
                "identifier": "NETFLIX001",
                "risk_level": "LOW",
                "is_verified": True
            },
            {
                "name": "Electricity Board",
                "category": "Utilities",
                "identifier": "EB001",
                "risk_level": "LOW",
                "is_verified": True
            },
            {
                "name": "Local Grocery",
                "category": "Grocery",
                "identifier": "GROCERY001",
                "risk_level": "LOW",
                "is_verified": True
            },
            {
                "name": "Unknown Merchant",
                "category": "Unknown",
                "identifier": "UNKNOWN001",
                "risk_level": "HIGH",
                "is_verified": False
            }
        ]

        for merchant_data in merchants:
            existing_merchant = db.query(Merchant).filter(
                Merchant.identifier == merchant_data["identifier"]
            ).first()

            if not existing_merchant:
                merchant = Merchant(
                    name=merchant_data["name"],
                    category=merchant_data["category"],
                    identifier=merchant_data["identifier"],
                    risk_level=merchant_data["risk_level"],
                    is_verified=merchant_data["is_verified"]
                )

                db.add(merchant)

        db.commit()

        print("Demo merchants created successfully")

finally:
    db.close()