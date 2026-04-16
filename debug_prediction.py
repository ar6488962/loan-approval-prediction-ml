import pickle
import numpy as np

# Load model
model = pickle.load(open("model.pkl", "rb"))

# User's exact inputs from the app:
# Income: 30,000, Co-income: 0, Loan: 100,000, Term: 360, Credit: 1 (Good)
# Gender: Male, Married: No, Dependents: 0, Education: Graduate
# Self-Employed: Yes, Property Area: Urban

print("=" * 70)
print("DEBUGGING: Testing User's Exact Inputs")
print("=" * 70)

# Construct feature vector exactly as app does
features_list = [
    30000,        # income
    0,            # coapplicant_income
    100000,       # loan_amount
    360,          # loan_term
    1,            # credit_history (1 = Good)
]

# Gender: Male
gender_female = 0  # "Male" != "Female"
gender_male = 1    # "Male" == "Male"
features_list.extend([gender_female, gender_male])

# Married: No
married_no = 1     # "No" == "No"
married_yes = 0    # "No" != "Yes"
features_list.extend([married_no, married_yes])

# Dependents: 0
dep_0 = 1      # "0" == "0"
dep_1 = 0
dep_2 = 0
dep_3plus = 0
features_list.extend([dep_0, dep_1, dep_2, dep_3plus])

# Education: Graduate
edu_graduate = 1       # "Graduate" == "Graduate"
edu_not_grad = 0
features_list.extend([edu_graduate, edu_not_grad])

# Self_Employed: Yes
self_emp_no = 0    # "Yes" != "No"
self_emp_yes = 1   # "Yes" == "Yes"
features_list.extend([self_emp_no, self_emp_yes])

# Property Area: Urban
prop_rural = 0         # "Urban" != "Rural"
prop_semiurban = 0     # "Urban" != "Semiurban"
prop_urban = 1         # "Urban" == "Urban"
features_list.extend([prop_rural, prop_semiurban, prop_urban])

print("\nFeature Vector:")
print(features_list)
print(f"\nLength: {len(features_list)}")

features_array = np.array(features_list).reshape(1, -1)

prediction = model.predict(features_array)[0]
proba = model.predict_proba(features_array)[0]

print("\n" + "=" * 70)
print("MODEL PREDICTION")
print("=" * 70)
print(f"Prediction: {prediction}")
print(f"Probabilities: {proba}")
print(f"Approval Probability: {proba[1]*100:.1f}%")
print(f"Rejection Probability: {proba[0]*100:.1f}%")

result = "✅ APPROVED" if prediction == 'Y' else "❌ REJECTED"
print(f"\nResult: {result}")

print("\n" + "=" * 70)
print("FEATURE BREAKDOWN")
print("=" * 70)
features_names = [
    "Income", "Co-Income", "Loan", "Term", "Credit",
    "Gender_Female", "Gender_Male",
    "Married_No", "Married_Yes",
    "Dep_0", "Dep_1", "Dep_2", "Dep_3+",
    "Edu_Graduate", "Edu_NotGrad",
    "SelfEmp_No", "SelfEmp_Yes",
    "Area_Rural", "Area_Semiurban", "Area_Urban"
]

for i, (name, val) in enumerate(zip(features_names, features_list)):
    print(f"Feature {i:2d}: {name:20s} = {val:>10}")
