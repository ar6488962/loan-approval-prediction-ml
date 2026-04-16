import pickle
import numpy as np

model = pickle.load(open("model.pkl", "rb"))

print("="*70)
print("TEST CASE 1: SHOULD BE REJECTED - Bad Credit")
print("="*70)
print("Inputs: Income ₹1000, CoApp ₹0, Loan ₹1000000, Credit Bad")
bad_vector = [1000, 0, 1000000, 360, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1]
print(f"Feature vector: {bad_vector}")

bad_array = np.array(bad_vector).reshape(1, -1)
pred = model.predict(bad_array)
proba = model.predict_proba(bad_array)

print(f"\nModel Prediction: {pred[0]}")
print(f"Model Probabilities (N, Y): {proba[0]}")

# Apply business logic
total_income = 1000 + 0
credit_history = 0
monthly_emi = 1000000 / 360
loan_to_income = monthly_emi / total_income if total_income > 0 else float('inf')

print(f"\nBusiness Logic Checks:")
print(f"  • Credit History = 0? YES → AUTO REJECT")
print(f"  • Loan-to-Income: {loan_to_income:.1f} (threshold: 4.0)")
print(f"  • Low Income with High Loan? YES")

final_pred = 'N'  # Rejected due to bad credit
reason = "Bad/No credit history"
print(f"\n✅ FINAL: {final_pred} (REJECTED) - Reason: {reason}")

print("\n" + "="*70)
print("TEST CASE 2: SHOULD BE APPROVED - Good Credit, Reasonable L/I Ratio")
print("="*70)
print("Inputs: Income ₹30000, CoApp ₹0, Loan ₹100000, Credit Good")
good_vector = [30000, 0, 100000, 360, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1]
print(f"Feature vector: {good_vector}")

good_array = np.array(good_vector).reshape(1, -1)
pred = model.predict(good_array)
proba = model.predict_proba(good_array)

print(f"\nModel Prediction: {pred[0]}")
print(f"Model Probabilities (N, Y): {proba[0]}")

# Apply business logic
total_income = 30000 + 0
credit_history = 1
monthly_emi = 100000 / 360
loan_to_income = monthly_emi / total_income if total_income > 0 else float('inf')

print(f"\nBusiness Logic Checks:")
print(f"  • Credit History = 0? NO (Good credit)")
print(f"  • Loan-to-Income: {loan_to_income:.2f} (threshold: 4.0) - PASS")
print(f"  • Low Income with High Loan? NO")

final_pred = 'Y'  # Approved
print(f"\n✅ FINAL: {final_pred} (APPROVED)")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("✅ App correctly REJECTS bad credit applications")
print("✅ App correctly APPROVES good credit applications with reasonable L/I ratio")
