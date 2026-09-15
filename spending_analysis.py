transactions = [
    {"category": "Food", "amount": 250},
    {"category": "Food", "amount": 450},
    {"category": "Shopping", "amount": 1200},
    {"category": "Transport", "amount": 300},
    {"category": "Food", "amount": 500},
    {"category": "Entertainment", "amount": 800},
]


# 1. Calculate total spending

total_spending = 0

for transaction in transactions:
    total_spending += transaction["amount"]


# 2. Calculate spending by category

category_spending = {}

for transaction in transactions:
    category = transaction["category"]
    amount = transaction["amount"]

    if category in category_spending:
        category_spending[category] += amount
    else:
        category_spending[category] = amount


# 3. Find highest spending category

highest_category = max(
    category_spending,
    key=category_spending.get
)


# 4. Savings analysis

monthly_income = 10000

remaining_money = monthly_income - total_spending


# 5. Display spending analysis

print("--- MONEY-MATE SPENDING ANALYSIS ---")

print("\nTotal spending: ₹", total_spending)

print("\nSpending by category:")

for category, amount in category_spending.items():
    print("-", category + ": ₹" + str(amount))

print("\nHighest spending category:", highest_category)


# 6. Savings insight

print("\n--- SAVINGS INSIGHT ---")

print("Monthly income: ₹", monthly_income)
print("Total spending: ₹", total_spending)
print("Remaining money: ₹", remaining_money)

if remaining_money > 0:
    print("Insight: You have ₹", remaining_money, "remaining after spending.")
elif remaining_money == 0:
    print("Insight: Your spending is equal to your income.")
else:
    print("Insight: Your spending is higher than your income.")


# 7. Ask MONEY-MATE a question

question = input("\nAsk MONEY-MATE: ").lower()

found_category = None

for category in category_spending:
    if category.lower() in question:
        found_category = category
        break


if "most" in question or "highest" in question:

    print("\nMONEY-MATE:")
    print(
        "Your highest spending category is",
        highest_category,
        "with ₹" + str(category_spending[highest_category]) + " spent."
    )

elif found_category:

    print("\nMONEY-MATE:")
    print(
        "You spent ₹" + str(category_spending[found_category]),
        "on", found_category + "."
    )

elif "total" in question:

    print("\nMONEY-MATE:")
    print("Your total spending is ₹" + str(total_spending) + ".")

else:

    print("\nMONEY-MATE:")
    print("I couldn't understand that question yet.")