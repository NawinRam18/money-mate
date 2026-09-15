amount = float(input("Enter transaction amount: ₹"))
merchant = input("Enter merchant name: ")
recipient_new = input("Is this a new recipient? (yes/no): ")
hour = int(input("Enter transaction hour (0-23): "))

risk_score = 0
reasons = []

# Rule 1: unusually high amount
if amount > 10000:
    risk_score += 30
    reasons.append("Transaction amount is unusually high")

# Rule 2: new recipient
if recipient_new.lower() == "yes":
    risk_score += 25
    reasons.append("Recipient is new")

# Rule 3: unusual transaction time
if hour < 6 or hour >= 23:
    risk_score += 20
    reasons.append("Transaction occurred at an unusual hour")

# Risk level
if risk_score <= 30:
    risk_level = "LOW"
elif risk_score <= 60:
    risk_level = "MEDIUM"
elif risk_score <= 80:
    risk_level = "HIGH"
else:
    risk_level = "CRITICAL"

# Decision
if risk_score >= 61:
    decision = "BLOCK"
elif risk_score >= 31:
    decision = "WARN"
else:
    decision = "APPROVE"

print("\n--- MONEY-MATE FRAUD ANALYSIS ---")
print("Risk Score:", risk_score, "/ 100")
print("Risk Level:", risk_level)
print("Decision:", decision)

print("\nReasons:")
if reasons:
    for reason in reasons:
        print("-", reason)
else:
    print("- No major suspicious signals detected")