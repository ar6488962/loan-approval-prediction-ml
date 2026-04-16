import pickle
import numpy as np

# Load model
model = pickle.load(open("model.pkl", "rb"))

# App's feature vector for: Income 1000, CoApp 0, Loan 1000000, Term 360, Credit 0, 
# Gender Male, Married No, Dependents 0, Education Graduate, Self_Employed No, Property Urban
app_vector = [1000, 0, 1000000, 360, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1]

print("App's feature vector:")
print(app_vector)
print(f"\nVector length: {len(app_vector)}")

# Convert to numpy array
app_array = np.array(app_vector).reshape(1, -1)

# Make prediction
pred = model.predict(app_array)
proba = model.predict_proba(app_array)

print(f"\nPrediction: {pred[0]}")
print(f"Probabilities (N, Y): {proba[0]}")
print(f"Approval Probability: {proba[0][1]*100:.1f}%")
print(f"Rejection Probability: {proba[0][0]*100:.1f}%")

print("\n\n" + "="*50)
print("Correct vector (from get_dummies) for Income 1000, CoApp 0, Loan 1000000:")

# This should match what pd.get_dummies creates
correct_vector = [1000, 0, 1000000, 360, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1]
print(correct_vector)

correct_array = np.array(correct_vector).reshape(1, -1)
pred2 = model.predict(correct_array)
proba2 = model.predict_proba(correct_array)

print(f"\nPrediction: {pred2[0]}")
print(f"Probabilities (N, Y): {proba2[0]}")
print(f"Approval Probability: {proba2[0][1]*100:.1f}%")

print("\n\n" + "="*50)
print("Model coefficients:")
print(model.coef_[0])
print("\nIntercept:", model.intercept_)

# Calculate decision function manually
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

score = np.dot(model.coef_[0], app_array.T) + model.intercept_
print(f"\nDecision function (raw score): {score[0]}")
print(f"Sigmoid of score: {sigmoid(score[0])[0]:.6f}")
print("(values > 0.5 mean APPROVED)")
