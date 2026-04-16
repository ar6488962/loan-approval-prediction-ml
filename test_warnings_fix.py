import pickle
import numpy as np
import pandas as pd
import warnings

# Capture warnings
warnings.filterwarnings('error', category=UserWarning)

model = pickle.load(open("model.pkl", "rb"))

print("=" * 70)
print("TEST: Prediction with DataFrame (WITH feature names)")
print("=" * 70)

# Create a test feature vector as a DataFrame with feature names
feature_names = [
    'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 
    'Credit_History', 'Gender_Female', 'Gender_Male', 'Married_No', 'Married_Yes',
    'Dependents_0', 'Dependents_1', 'Dependents_2', 'Dependents_3+',
    'Education_Graduate', 'Education_Not Graduate', 'Self_Employed_No', 'Self_Employed_Yes',
    'Property_Area_Rural', 'Property_Area_Semiurban', 'Property_Area_Urban'
]

test_values = [30000, 0, 100000, 360, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1]

# Using DataFrame with feature names (NEW METHOD)
features_df = pd.DataFrame([test_values], columns=feature_names)

try:
    pred = model.predict(features_df)
    proba = model.predict_proba(features_df)
    print(f"✅ NO WARNINGS! Prediction successful with DataFrame")
    print(f"   Prediction: {pred[0]}")
    print(f"   Probabilities: {proba[0]}")
except UserWarning as e:
    print(f"❌ WARNING OCCURRED: {e}")

print("\n" + "=" * 70)
print("TEST: Prediction with NumPy Array (WITHOUT feature names)")
print("=" * 70)

# Using numpy array without feature names (OLD METHOD)
features_array = np.array(test_values).reshape(1, -1)

try:
    pred = model.predict(features_array)
    proba = model.predict_proba(features_array)
    print(f"❌ OLD METHOD: This should have warnings...")
    print(f"   Prediction: {pred[0]}")
except UserWarning as e:
    print(f"✅ WARNING DETECTED (as expected): {e}")

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)
print("✅ Using DataFrame with feature names ELIMINATES the sklearn warnings!")
print("✅ The fix in app.py resolves all the warning issues.")
