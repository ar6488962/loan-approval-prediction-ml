import pickle
import pandas as pd
import numpy as np

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Show model properties
print("Model Classes:", model.classes_)
print("Model Features Expected:", model.n_features_in_)
print("\nModel Coefficients Shape:", model.coef_.shape)
print("Model Coefficients:", model.coef_)

# Load training data to understand feature order
train = pd.read_csv("train_u6lujuX_CVtuZ9i.csv")

# Perform same preprocessing as notebook
train = train.drop('Loan_ID', axis=1)

# Create feature engineering (same as notebook)
train['Total_Income'] = train['ApplicantIncome'] + train['CoapplicantIncome']
train['EMI'] = (train['LoanAmount'] / train['Loan_Amount_Term']).fillna(0)
train['Balance Income'] = train['Total_Income'] - (train['EMI'] * 1000)

# Drop the original variables (same as notebook)
train = train.drop(['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term'], axis=1)

# Get dummies (same as notebook)
X = train.drop('Loan_Status', axis=1)
X = pd.get_dummies(X)

print("\n\nX.shape after get_dummies:", X.shape)
print("X.columns:", X.columns.tolist())

# Test with first row
test_row = X.iloc[0:1]
print("\n\nFirst row values:")
print(test_row.values)

pred = model.predict(test_row)
print("Prediction for first row:", pred)
print("Probabilities:", model.predict_proba(test_row))

# Test with a specific case: Bad credit, high loan amount
bad_credit_case = X.iloc[0:1].copy()
print("\n\nTesting with high loan amount and low income...")

# Try to construct manually
print("\n\nManually constructed feature vector:")
print("Number of features needed:", model.n_features_in_)
