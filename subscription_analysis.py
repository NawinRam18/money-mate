transactions = [
    {"merchant": "Netflix", "amount": 499},
    {"merchant": "Spotify", "amount": 119},
    {"merchant": "Amazon", "amount": 299},
    {"merchant": "Netflix", "amount": 499},
    {"merchant": "Spotify", "amount": 119},
    {"merchant": "Amazon", "amount": 299},
]


# Find recurring merchants

merchant_payments = {}

for transaction in transactions:
    merchant = transaction["merchant"]
    amount = transaction["amount"]

    if merchant in merchant_payments:
        merchant_payments[merchant] += 1
    else:
        merchant_payments[merchant] = 1


# Identify subscriptions

subscriptions = []

for merchant, count in merchant_payments.items():
    if count >= 2:
        subscriptions.append(merchant)


# Calculate subscription spending

subscription_spending = 0

for transaction in transactions:
    if transaction["merchant"] in subscriptions:
        subscription_spending += transaction["amount"]


# Display results

print("--- MONEY-MATE SUBSCRIPTION ANALYSIS ---")

print("\nRecurring subscriptions:")

for subscription in subscriptions:
    print("-", subscription)

print("\nNumber of subscriptions:", len(subscriptions))

print("Total recurring payment amount: ₹", subscription_spending)

print("\nMONEY-MATE INSIGHT:")

if subscriptions:
    print(
        "You have",
        len(subscriptions),
        "recurring subscriptions."
    )
    print(
        "Your total recurring payment amount is ₹",
        subscription_spending
    )
else:
    print("No recurring subscriptions detected.")