import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Load data
train = pd.read_csv("train_u6lujuX_CVtuZ9i.csv")

# Drop Loan_ID
train = train.drop('Loan_ID', axis=1)

# Handle missing values
train = train.fillna(0)

# Separate target and features
y = train['Loan_Status']
X = train.drop('Loan_Status', axis=1)

# Get dummies WITHOUT drop_first to keep all categories (20 features)
X = pd.get_dummies(X, drop_first=False)

print("Feature columns after get_dummies(drop_first=True):")
for i, col in enumerate(X.columns):
    print(f"{i}: {col}")

print(f"\nShape: {X.shape}")

# Split data
x_train, x_cv, y_train, y_cv = train_test_split(X, y, test_size=0.3, random_state=0)

# Ensure no missing values
x_train = x_train.fillna(0)
x_cv = x_cv.fillna(0)

# Train model
model = LogisticRegression(random_state=1, max_iter=1000)
model.fit(x_train, y_train)

# Check accuracy
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

cv_pred = model.predict(x_cv)
cv_acc = accuracy_score(y_cv, cv_pred)

print(f"\nCV Accuracy: {cv_acc:.4f}")

print("\nModel Coefficients:")
for i, col in enumerate(X.columns):
    coef = model.coef_[0][i]
    print(f"{i} ({col}): {coef:8.6f}")

# Save the model
pickle.dump(model, open("model.pkl", "wb"))
print("\n✅ Model saved to model.pkl")
