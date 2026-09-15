def spending_tool():
    transactions = [
        {"category": "Food", "amount": 250},
        {"category": "Food", "amount": 450},
        {"category": "Shopping", "amount": 1200},
        {"category": "Transport", "amount": 300},
        {"category": "Food", "amount": 500},
        {"category": "Entertainment", "amount": 800},
    ]

    total = sum(t["amount"] for t in transactions)

    category_spending = {}

    for transaction in transactions:
        category = transaction["category"]
        amount = transaction["amount"]

        category_spending[category] = (
            category_spending.get(category, 0) + amount
        )

    highest_category = max(
        category_spending,
        key=category_spending.get
    )

    return total, category_spending, highest_category


def subscription_tool():
    transactions = [
        {"merchant": "Netflix", "amount": 499},
        {"merchant": "Spotify", "amount": 119},
        {"merchant": "Amazon", "amount": 299},
        {"merchant": "Netflix", "amount": 499},
        {"merchant": "Spotify", "amount": 119},
        {"merchant": "Amazon", "amount": 299},
    ]

    merchant_payments = {}

    for transaction in transactions:
        merchant = transaction["merchant"]

        merchant_payments[merchant] = (
            merchant_payments.get(merchant, 0) + 1
        )

    subscriptions = []

    for merchant, count in merchant_payments.items():
        if count >= 2:
            subscriptions.append(merchant)

    return subscriptions


def blocked_payment_tool():
    risk_score = 100
    risk_level = "CRITICAL"
    decision = "BLOCK"

    reasons = [
        "Transaction amount is unusually high",
        "Recipient is new",
        "Transaction occurred at an unusual hour"
    ]

    return risk_score, risk_level, decision, reasons


# Main assistant

question = input("Ask MONEY-MATE: ").lower()

if "subscription" in question:
    subscriptions = subscription_tool()

    print("\nMONEY-MATE:")
    print("You have", len(subscriptions), "recurring subscriptions.")

    for subscription in subscriptions:
        print("-", subscription)


elif "blocked" in question or "payment" in question:

    risk_score, risk_level, decision, reasons = blocked_payment_tool()

    print("\nMONEY-MATE:")
    print("This payment was blocked because it was considered highly risky.")

    print("\nReasons:")
    for reason in reasons:
        print("-", reason)


else:

    total, category_spending, highest_category = spending_tool()

    print("\nMONEY-MATE:")

    if "most" in question or "highest" in question:
        print(
            "Your highest spending category is",
            highest_category,
            "with ₹",
            category_spending[highest_category]
        )

    elif "total" in question:
        print("Your total spending is ₹", total)

    else:
        print("Your spending by category is:")

        for category, amount in category_spending.items():
            print("-", category, ": ₹", amount)