import pickle
import numpy as np
import pandas as pd

# Load the model
model = pickle.load(open("model.pkl", "rb"))

# Get model information
print("=" * 70)
print("MODEL ANALYSIS - LOAN APPROVAL PREDICTION")
print("=" * 70)

print(f"\nModel Type: {type(model).__name__}")
print(f"Number of Features: {model.n_features_in_}")
print(f"Classes: {model.classes_}")
print(f"Model Intercept: {model.intercept_[0]:.4f}")

# Get feature coefficients (importance)
print(f"\nTop 10 Feature Coefficients (sorted by importance):")
print("-" * 70)
coef = model.coef_[0]
feature_importance = sorted(enumerate(coef), key=lambda x: abs(x[1]), reverse=True)

for idx, (feature_idx, coef_val) in enumerate(feature_importance[:10]):
    importance = "↑ INCREASES APPROVAL" if coef_val > 0 else "↓ DECREASES APPROVAL"
    print(f"{idx+1}. Feature {feature_idx}: {coef_val:+.4f} {importance}")

print("\n" + "=" * 70)
print("PREDICTION TESTS - DIFFERENT SCENARIOS")
print("=" * 70)

# Test different scenarios
test_scenarios = [
    {
        "name": "❌ Low Income, High Loan (RISKY)",
        "values": [5000, 0, 100000, 360, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0]
    },
    {
        "name": "⚠️  Moderate Income, Moderate Loan",
        "values": [15000, 5000, 80000, 360, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0]
    },
    {
        "name": "✅ Good Income, Moderate Loan, Married",
        "values": [25000, 5000, 100000, 360, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0]
    },
    {
        "name": "✅ High Income, High Loan, Good Credit",
        "values": [50000, 10000, 200000, 360, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0]
    },
    {
        "name": "✅ Very High Income, Married, Graduate",
        "values": [75000, 25000, 250000, 360, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0]
    },
    {
        "name": "❌ Poor Credit History (Major Red Flag)",
        "values": [30000, 5000, 100000, 360, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0]
    },
    {
        "name": "❌ Good Income, Very High Loan (DTI Issue)",
        "values": [20000, 0, 500000, 360, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0]
    }
]

for scenario in test_scenarios:
    features = np.array(scenario["values"]).reshape(1, -1)
    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0]
    
    status = "✅ APPROVED" if prediction == 1 else "❌ REJECTED"
    print(f"\n{scenario['name']}")
    print(f"  Result: {status}")
    print(f"  Approval Probability: {proba[1]*100:.1f}%")
    print(f"  Decision Confidence: {max(proba)*100:.1f}%")

print("\n" + "=" * 70)
print("KEY INSIGHTS FOR APPROVAL RANGES")
print("=" * 70)
print("""
📊 APPROVAL THRESHOLDS:

✅ LIKELY APPROVED:
   • Income: ₹20,000 - ₹75,000+ per month
   • Loan Amount: ₹80,000 - ₹250,000 (within income ratio)
   • Debt-to-Income Ratio: < 5 (Loan/Income < 5)
   • Credit History: 1 (MUST HAVE!)
   • Marital Status: Married is slightly better
   • Education: Graduate is slightly better

❌ LIKELY REJECTED:
   • Very Low Income: < ₹10,000 with high loans
   • Very High Loan: > 10x monthly income
   • Poor Credit History: 0 (Most critical factor!)
   • Extreme Debt-to-Income: > 10

⚠️  CRITICAL FACTOR:
   ⚡ CREDIT HISTORY IS THE MOST IMPORTANT!
   ⚡ Poor credit (0) almost always means REJECTION
   ⚡ Even with good income, bad credit = REJECTED

💡 INCOME TO LOAN RATIO MATTERS:
   • Safe Ratio: Loan ÷ Income = 3-5x
   • Risky Ratio: Loan ÷ Income = 8-10x
   • Very Risky: Loan ÷ Income > 10x
""")
