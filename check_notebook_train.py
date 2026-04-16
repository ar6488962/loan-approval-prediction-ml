import pickle
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load training data
train = pd.read_csv("train_u6lujuX_CVtuZ9i.csv")
test = pd.read_csv("test_Y3wMUE5_7gLdaTN.csv")

# Drop Loan_ID (EXACT notebook preprocessing)
train = train.drop('Loan_ID', axis=1)
test = test.drop('Loan_ID', axis=1)

# Separate target
X = train.drop('Loan_Status', axis=1)
y = train['Loan_Status']

# Get dummies (EXACT notebook method)
X = pd.get_dummies(X)
test = pd.get_dummies(test)

print("Features from notebook preprocessing:")
for i, col in enumerate(X.columns):
    print(f"{i}: {col}")
print(f"\nTotal: {X.shape[1]} features")

# Split and fill missing (EXACT notebook method)
x_train, x_cv, y_train, y_cv = train_test_split(X, y, test_size=0.3, random_state=0)
x_train = x_train.fillna(0)
x_cv = x_cv.fillna(0)

# Train model (EXACT notebook method)
model = LogisticRegression(random_state=1)
model.fit(x_train, y_train)

# Get accuracy
pred_cv = model.predict(x_cv)
accuracy = accuracy_score(y_cv, pred_cv)

print(f"\n✅ Model trained with CV Accuracy: {accuracy:.4f}")
print(f"Model Classes: {model.classes_}")

print("\nCoefficients:")
for i, col in enumerate(X.columns):
    coef = model.coef_[0][i]
    if i < 5:  # Show first 5
        print(f"{i} ({col}): {coef:10.6f}")
    elif i == 5:
        print("...")

# Save
pickle.dump(model, open("model.pkl", "wb"))
print("\n✅ Model saved")

# Now test with the app's feature vector
print("\n" + "="*60)
print("TESTING APP VECTORS")
print("="*60)

# App constructs features in this order:
# 0-4: Income, CoIncome, Loan, Term, Credit
# 5-6: Gender_Female, Gender_Male
# 7-8: Married_No, Married_Yes
# 9-12: Dep_0, Dep_1, Dep_2, Dep_3+
# 13-14: Edu_Grad, Edu_NotGrad
# 15-16: SelfEmp_No, SelfEmp_Yes
# 17-19: Area_Rural, Area_Semiurban, Area_Urban

# Test case: Bad case (should reject)
bad_vector = [1000, 0, 1000000, 360, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1]

print(f"\nBad test case vector (20 features):")
print(f"Vector: {bad_vector}")

bad_array = np.array(bad_vector).reshape(1, -1)
try:
    pred = model.predict(bad_array)
    print(f"ERROR: Prediction worked with {model.n_features_in_} features, but app provided 20!")
except:
    print(f"Good: Model expects {model.n_features_in_} features, app provides 20")
    print("Feature mismatch detected - need to match feature order exactly")
