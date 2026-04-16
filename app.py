import streamlit as st
import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

# Set page config
st.set_page_config(
    page_title="Loan Approval Prediction",
    page_icon="🏦",
    layout="wide"
)

# Load model
try:
    model = pickle.load(open("model.pkl", "rb"))
except:
    st.error("Error: Could not load model.pkl file. Please ensure the file exists in the directory.")
    st.stop()

# Page title and description
st.title("🏦 Loan Approval Prediction App")
st.markdown("---")
st.write("""
This app predicts whether a bank loan application will be approved or rejected based on 
applicant information using a trained Logistic Regression model.
""")

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.header("📋 Personal Information")
    
    # Gender
    gender = st.selectbox(
        "Gender",
        ["Male", "Female"],
        help="Applicant's gender"
    )
    
    # Marital Status
    married = st.selectbox(
        "Marital Status",
        ["No", "Yes"],
        help="Is the applicant married?"
    )
    
    # Dependents
    dependents = st.selectbox(
        "Number of Dependents",
        ["0", "1", "2", "3+"],
        help="Number of dependents (including spouse and children)"
    )
    
    # Education
    education = st.selectbox(
        "Education Level",
        ["Graduate", "Not Graduate"],
        help="Highest education level"
    )
    
    # Employment Status
    self_employed = st.selectbox(
        "Employment Type",
        ["No", "Yes"],
        help="Is the applicant self-employed?"
    )

with col2:
    st.header("💰 Financial Information")
    
    # Applicant Income
    income = st.number_input(
        "Applicant Income (Monthly, in currency units)",
        min_value=0,
        max_value=1000000,
        value=5000,
        step=100,
        help="Monthly salary of the applicant (typical range: 2000-20000)"
    )
    
    # Co-applicant Income
    coapplicant_income = st.number_input(
        "Co-applicant Income (Monthly, in currency units)",
        min_value=0,
        max_value=1000000,
        value=0,
        step=100,
        help="Monthly salary of co-applicant if applicable"
    )
    
    # Loan Amount
    loan_amount = st.number_input(
        "Loan Amount (in currency units)",
        min_value=0,
        max_value=1000000,
        value=50000,
        step=1000,
        help="Total loan amount requested (typical range: 20000-500000)"
    )
    
    # Loan Term
    loan_term = st.selectbox(
        "Loan Amount Term (Months)",
        [360, 180, 120, 240, 60],
        help="Duration of the loan in months"
    )

st.markdown("---")

# Credit History Section
st.header("📊 Credit Information")
col_credit = st.columns(1)[0]
with col_credit:
    credit_history = st.selectbox(
        "Credit History",
        [1, 0],
        format_func=lambda x: "Good (1)" if x == 1 else "Bad/No History (0)",
        help="Does the applicant have a good credit history? (1=Yes, 0=No)"
    )

st.markdown("---")

# Property Area
st.header("🏠 Property Details")
col_property = st.columns(1)[0]
with col_property:
    property_area = st.selectbox(
        "Property Area",
        ["Urban", "Semiurban", "Rural"],
        help="Type of area where the property is located"
    )

st.markdown("---")

# Prediction Button
col_button = st.columns([1, 1, 1])
with col_button[1]:
    predict_button = st.button(
        "🔮 Predict Loan Status",
        use_container_width=True,
        type="primary"
    )

# Process prediction
if predict_button:
    try:
        # Create feature vector matching training data structure
        # EXACT feature order from pd.get_dummies() applied to original training data:
        # 0: ApplicantIncome
        # 1: CoapplicantIncome
        # 2: LoanAmount
        # 3: Loan_Amount_Term
        # 4: Credit_History
        # 5-6: Gender (Female, Male)
        # 7-8: Married (No, Yes)
        # 9-12: Dependents (0, 1, 2, 3+)
        # 13-14: Education (Graduate, Not Graduate)
        # 15-16: Self_Employed (No, Yes)
        # 17-19: Property_Area (Rural, Semiurban, Urban)
        
        # Build feature list in exact order
        features_list = [
            income,                  # 0: ApplicantIncome
            coapplicant_income,      # 1: CoapplicantIncome
            loan_amount,             # 2: LoanAmount
            loan_term,               # 3: Loan_Amount_Term
            credit_history           # 4: Credit_History
        ]
        
        # Encode Gender - 5-6: Gender_Female, Gender_Male
        gender_female = 1 if gender == "Female" else 0
        gender_male = 1 if gender == "Male" else 0
        features_list.extend([gender_female, gender_male])
        
        # Encode Married - 7-8: Married_No, Married_Yes
        married_no = 1 if married == "No" else 0
        married_yes = 1 if married == "Yes" else 0
        features_list.extend([married_no, married_yes])
        
        # Encode Dependents - 9-12: Dependents_0, 1, 2, 3+
        dep_0 = 1 if dependents == "0" else 0
        dep_1 = 1 if dependents == "1" else 0
        dep_2 = 1 if dependents == "2" else 0
        dep_3plus = 1 if dependents == "3+" else 0
        features_list.extend([dep_0, dep_1, dep_2, dep_3plus])
        
        # Encode Education - 13-14: Education_Graduate, Not Graduate
        edu_graduate = 1 if education == "Graduate" else 0
        edu_not_grad = 1 if education == "Not Graduate" else 0
        features_list.extend([edu_graduate, edu_not_grad])
        
        # Encode Self_Employed - 15-16: Self_Employed_No, Yes
        self_emp_no = 1 if self_employed == "No" else 0
        self_emp_yes = 1 if self_employed == "Yes" else 0
        features_list.extend([self_emp_no, self_emp_yes])
        
        # Encode Property_Area - 17-19: Property_Area_Rural, Semiurban, Urban
        prop_rural = 1 if property_area == "Rural" else 0
        prop_semiurban = 1 if property_area == "Semiurban" else 0
        prop_urban = 1 if property_area == "Urban" else 0
        features_list.extend([prop_rural, prop_semiurban, prop_urban])
        
        # Convert to DataFrame with proper feature names to avoid sklearn warnings
        # The model was trained with feature names from pd.get_dummies()
        feature_names = [
            'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 
            'Credit_History', 'Gender_Female', 'Gender_Male', 'Married_No', 'Married_Yes',
            'Dependents_0', 'Dependents_1', 'Dependents_2', 'Dependents_3+',
            'Education_Graduate', 'Education_Not Graduate', 'Self_Employed_No', 'Self_Employed_Yes',
            'Property_Area_Rural', 'Property_Area_Semiurban', 'Property_Area_Urban'
        ]
        features_df = pd.DataFrame([features_list], columns=feature_names)
        
        # Debug: Show feature vector for verification
        with st.expander("🔍 Debug Info (Feature Vector)", expanded=False):
            st.write(f"**Feature Vector Values:** {features_list}")
            st.write(f"**Vector Shape:** {features_df.shape}")
            st.write(f"**Model Expected Features:** {model.n_features_in_}")
        
        st.info(f"📊 Feature vector shape: {features_df.shape}")
        st.info(f"📊 Model expected features: {model.n_features_in_}")
        
        # Make prediction
        prediction = model.predict(features_df)
        prediction_proba = model.predict_proba(features_df)
        
        # APPLY BUSINESS LOGIC VALIDATION
        # The model was trained on data with potential biases, so apply sanity checks
        total_income = income + coapplicant_income
        
        # Override prediction with business rules
        business_rejection_reason = None
        final_prediction = prediction[0]  # Start with model prediction
        
        # Rule 0: Edge case validation - Zero income or zero loan amount
        if total_income == 0:
            final_prediction = 'N'
            business_rejection_reason = "Applicant has zero income"
        elif loan_amount == 0:
            final_prediction = 'N'
            business_rejection_reason = "Loan amount cannot be zero"
        
        # Rule 1: If credit history is bad (0), automatically reject
        elif credit_history == 0:
            final_prediction = 'N'
            business_rejection_reason = "Bad/No credit history"
        
        # Rule 2: Loan-to-Income ratio should be < 4.0 for approval
        # (i.e., monthly income should be at least 25% of monthly loan payment)
        elif total_income > 0:
            monthly_emi = loan_amount / loan_term  # Simplified EMI calculation
            loan_to_income = monthly_emi / total_income
            if loan_to_income > 4.0 and final_prediction == 'Y':
                final_prediction = 'N'
                business_rejection_reason = f"Loan-to-Income ratio too high ({loan_to_income:.2f})"
            # Rule 3: Minimum income threshold
            elif total_income < 5000 and loan_amount > 100000:
                final_prediction = 'N'
                business_rejection_reason = "Income too low for requested loan amount"
        
        # Display results
        st.markdown("---")
        st.header("📈 Prediction Results")
        
        result_col1, result_col2, result_col3 = st.columns(3)
        
        with result_col1:
            # Show final prediction (after business logic)
            if final_prediction == 'Y':
                st.success("✅ LOAN APPROVED", icon="✅")
            else:
                st.error("❌ LOAN REJECTED", icon="❌")
        
        # Show rejection reason if applicable
        if business_rejection_reason:
            st.warning(f"⚠️ **Rejection Reason:** {business_rejection_reason}")
        
        with result_col2:
            # Probabilities are in order of classes: ['N', 'Y']
            # So proba[0] = rejection, proba[1] = approval
            approval_probability = prediction_proba[0][1] * 100
            st.metric("Approval Probability", f"{approval_probability:.1f}%")
        
        with result_col3:
            rejection_probability = prediction_proba[0][0] * 100
            st.metric("Rejection Probability", f"{rejection_probability:.1f}%")
        
        # Display confidence
        st.markdown("---")
        confidence = max(prediction_proba[0]) * 100
        st.write(f"**Model Confidence:** {confidence:.1f}%")
        
        # Input Summary
        st.markdown("---")
        st.subheader("📋 Application Summary")
        
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.write(f"**Gender:** {gender}")
            st.write(f"**Marital Status:** {married}")
            st.write(f"**Dependents:** {dependents}")
            st.write(f"**Education:** {education}")
            st.write(f"**Employment:** {'Self-Employed' if self_employed == 'Yes' else 'Regular Employee'}")
        
        with summary_col2:
            st.write(f"**Income:** ₹{income:,.0f}")
            st.write(f"**Co-applicant Income:** ₹{coapplicant_income:,.0f}")
            st.write(f"**Total Income:** ₹{income + coapplicant_income:,.0f}")
            st.write(f"**Loan Amount:** ₹{loan_amount:,.0f}")
            st.write(f"**Loan Term:** {loan_term} months")
            st.write(f"**Property Area:** {property_area}")
            st.write(f"**Credit History:** {'Good' if credit_history == 1 else 'Bad/None'}")

    except Exception as e:
        st.error(f"❌ Error during prediction: {str(e)}")
        st.info("Please ensure all fields are filled correctly and try again.")
