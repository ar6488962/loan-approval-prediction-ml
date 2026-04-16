import pandas as pd
import pickle
import numpy as np

# Load and prepare training data exactly as in notebook
train = pd.read_csv("train_u6lujuX_CVtuZ9i.csv")
test = pd.read_csv("test_Y3wMUE5_7gLdaTN.csv")

# Drop Loan_ID
train = train.drop('Loan_ID', axis=1)
test_data = test.drop('Loan_ID', axis=1)

# Separate target
X = train.drop('Loan_Status', axis=1)
y = train.Loan_Status

# Apply get_dummies WITHOUT any preprocessing
X = pd.get_dummies(X)
test_data = pd.get_dummies(test_data)

print("Column order from pd.get_dummies():")
for i, col in enumerate(X.columns):
    print(f"{i}: {col}")

print(f"\nTotal columns: {len(X.columns)}")

# Load model and check
model = pickle.load(open("model.pkl", "rb"))
print(f"Model expects {model.n_features_in_} features")
print(f"X has {X.shape[1]} features")

# Try to predict
from sklearn.model_selection import train_test_split
x_train, x_cv, y_train, y_cv = train_test_split(X, y, test_size=0.3, random_state=0)
x_train = x_train.fillna(0)
x_cv = x_cv.fillna(0)

pred = model.predict(x_cv)
print(f"Prediction works! Predictions shape: {pred.shape}")

# Now test with manual features
print("\n\nManually constructing features for test case:")
print("Income: 1000, CoApp: 1000, Loan: 1000000, Term: 360, Credit: 0")

# Features in correct order from get_dummies
manual_features = [
    0,  # Credit_History = 0 (Bad)
    1000,  # ApplicantIncome
    1000,  # CoapplicantIncome
    1000000,  # LoanAmount
    360,  # Loan_Amount_Term
    0,  # Gender_Female (Male selected, so 0)
    1,  # Gender_Male (Male selected, so 1)
    1,  # Married_No (No selected, so 1)
    0,  # Married_Yes
    0,  # Dependents_0
    1,  # Dependents_1
    0,  # Dependents_2
    0,  # Dependents_3+
    0,  # Education_Graduate
    1,  # Education_Not Graduate
    1,  # Self_Employed_No (Regular Employee, so 1)
    0,  # Self_Employed_Yes
    0,  # Property_Area_Rural
    0,  # Property_Area_Semiurban
    1   # Property_Area_Urban
]

manual_array = np.array(manual_features).reshape(1, -1)
print(f"\nFeature vector: {manual_features}")
print(f"Shape: {manual_array.shape}")

pred = model.predict(manual_array)
proba = model.predict_proba(manual_array)
print(f"\nPrediction: {pred}")
print(f"Probabilities (N, Y): {proba}")
print(f"Approval: {proba[0][1]*100:.1f}%")
