# Transaction result from our fraud detection system

risk_score = 100
risk_level = "CRITICAL"
decision = "BLOCK"

reasons = [
    "Transaction amount is unusually high",
    "Recipient is new",
    "Transaction occurred at an unusual hour"
]


print("--- MONEY-MATE TRANSACTION EXPLANATION ---")

print("\nRisk Score:", risk_score, "/ 100")
print("Risk Level:", risk_level)
print("Decision:", decision)


# Explain the decision

print("\nMONEY-MATE:")

if decision == "BLOCK":

    print("This payment was blocked because it was considered highly risky.")

    print("\nReasons:")

    for reason in reasons:
        print("-", reason)

elif decision == "WARN":

    print("This payment has some suspicious signals.")

    print("\nReasons:")

    for reason in reasons:
        print("-", reason)

else:

    print("This payment was approved because no major risk was detected.")