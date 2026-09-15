import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import IsolationForest
data = {
    "amount": [
        200, 500, 350, 1000, 750, 300,
        15000, 25000, 18000, 12000, 30000, 22000,
        400, 800, 600, 1200, 900, 250,
        20000, 16000, 28000, 14000, 35000, 19000
    ],

    "new_recipient": [
        0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1
    ],

    "hour": [
        14, 18, 12, 10, 16, 20,
        2, 3, 1, 23, 4, 2,
        11, 15, 13, 17, 19, 21,
        1, 5, 0, 3, 2, 4
    ],

    "fraud": [
        0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1
    ]
}

df = pd.DataFrame(data)

print("Dataset:")
print(df)

print("\nNumber of transactions:", len(df))
print("Fraud transactions:", df["fraud"].sum())
print("Normal transactions:", len(df) - df["fraud"].sum())

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Features used by the ML model
features = ["amount", "new_recipient", "hour"]

X = df[features]
y = df["fraud"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# Create the ML model
model = LogisticRegression()

# Train the model
model.fit(X_train, y_train)
# Create anomaly detection model
anomaly_model = IsolationForest(
    contamination=0.2,
    random_state=42
)

# Train anomaly detector
anomaly_model.fit(X_train)

# Check the new transaction
anomaly_prediction = anomaly_model.predict(new_transaction)

if anomaly_prediction[0] == -1:
    anomaly_result = "ANOMALY"
else:
    anomaly_result = "NORMAL"

print("Anomaly result:", anomaly_result)
# Test the model
predictions = model.predict(X_test)

# Measure accuracy
accuracy = accuracy_score(y_test, predictions)

print("\n--- ML MODEL RESULTS ---")
print("Accuracy:", round(accuracy * 100, 2), "%")
# Test the model with a new transaction

new_transaction = pd.DataFrame({
    "amount": [25000],
    "new_recipient": [1],
    "hour": [2]
})

fraud_probability = model.predict_proba(new_transaction)[0][1]

# Convert probability to a 0-100 risk score
risk_score = round(fraud_probability * 100)

# Determine risk level
if risk_score <= 30:
    risk_level = "LOW"
elif risk_score <= 60:
    risk_level = "MEDIUM"
elif risk_score <= 80:
    risk_level = "HIGH"
else:
    risk_level = "CRITICAL"

# Determine decision
if risk_score >= 61:
    decision = "BLOCK"
elif risk_score >= 31:
    decision = "WARN"
else:
    decision = "APPROVE"

print("\n--- MONEY-MATE AI RISK ANALYSIS ---")
print("Amount: ₹25,000")
print("New recipient: Yes")
print("Transaction hour: 2 AM")
print("Fraud probability:", round(fraud_probability * 100, 2), "%")
print("Risk score:", risk_score, "/ 100")
print("Risk level:", risk_level)
print("Decision:", decision)
# Generate human-readable reasons
reasons = []

if new_transaction["amount"].iloc[0] > 10000:
    reasons.append("Transaction amount is unusually high")

if new_transaction["new_recipient"].iloc[0] == 1:
    reasons.append("Recipient is new")

hour = new_transaction["hour"].iloc[0]

if hour < 6 or hour >= 23:
    reasons.append("Transaction occurred at an unusual hour")

print("\nWhy is this transaction risky?")

if reasons:
    for reason in reasons:
        print("•", reason)
else:
    print("• No major suspicious signals detected")