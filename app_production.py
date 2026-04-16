"""
Loan Approval Prediction App - Production Version
A professional Streamlit web application for predicting loan approval status.

Features:
- Machine learning model integration (Logistic Regression)
- Professional UI with proper error handling
- Input validation with realistic constraints
- Business logic rules for approval decisions
- Comprehensive application summary
"""

import streamlit as st
import numpy as np
import pandas as pd
import pickle
import os
import logging
from typing import Tuple, Dict, Any
from pathlib import Path

# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(
    page_title="Loan Approval Prediction",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# CONSTANTS & CONFIGURATION
# ============================================================================

MODEL_PATH = "model.pkl"
FEATURE_NAMES = [
    'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term',
    'Credit_History', 'Gender_Female', 'Gender_Male', 'Married_No', 'Married_Yes',
    'Dependents_0', 'Dependents_1', 'Dependents_2', 'Dependents_3+',
    'Education_Graduate', 'Education_Not Graduate', 'Self_Employed_No',
    'Self_Employed_Yes', 'Property_Area_Rural', 'Property_Area_Semiurban',
    'Property_Area_Urban'
]

# Input validation ranges
INPUT_RANGES = {
    'income': (0, 1000000, 'Monthly Income'),
    'coapplicant_income': (0, 1000000, 'Co-applicant Income'),
    'loan_amount': (1, 1000000, 'Loan Amount'),  # Minimum 1 (not 0)
    'loan_term': (12, 480, 'Loan Term'),
}

# Business rules thresholds
BUSINESS_RULES = {
    'min_income_for_high_loan': 5000,
    'high_loan_threshold': 100000,
    'max_loan_to_income_ratio': 4.0,
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_resource
def load_model() -> Any:
    """
    Load the pre-trained ML model with caching for performance.
    
    Returns:
        The loaded model object
        
    Raises:
        FileNotFoundError: If model.pkl doesn't exist
        pickle.UnpicklingError: If model.pkl is corrupted
    """
    try:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found in the application directory.")
        
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        
        logger.info(f"✅ Model loaded successfully. Features: {model.n_features_in_}")
        return model
        
    except FileNotFoundError as e:
        logger.error(f"❌ Model file error: {e}")
        raise
    except pickle.UnpicklingError as e:
        logger.error(f"❌ Model corruption error: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error loading model: {e}")
        raise


def validate_inputs(income: float, coapplicant_income: float, loan_amount: float,
                   loan_term: int) -> Tuple[bool, str]:
    """
    Validate user inputs against realistic constraints.
    
    Args:
        income: Applicant's monthly income
        coapplicant_income: Co-applicant's monthly income
        loan_amount: Requested loan amount
        loan_term: Loan term in months
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check loan amount is positive
    if loan_amount <= 0:
        return False, "❌ Loan amount must be greater than zero."
    
    # Check total income is reasonable
    total_income = income + coapplicant_income
    if total_income < 500:  # Minimum monthly income
        return False, "❌ Total monthly income must be at least ₹500."
    
    # Check loan term is valid
    if loan_term not in [60, 120, 180, 240, 360]:
        return False, "❌ Invalid loan term selected."
    
    # Check income to loan ratio is reasonable
    max_reasonable_loan = total_income * 12 * 10  # Up to 10 years of income
    if loan_amount > max_reasonable_loan:
        return False, f"❌ Loan amount (₹{loan_amount:,.0f}) seems unrealistic for total income of ₹{total_income:,.0f}/month."
    
    return True, ""


def encode_categorical_features(gender: str, married: str, dependents: str,
                               education: str, self_employed: str,
                               property_area: str) -> list:
    """
    Encode categorical features using one-hot encoding.
    
    Args:
        gender: Applicant's gender
        married: Marital status
        dependents: Number of dependents
        education: Education level
        self_employed: Employment type
        property_area: Property location area
        
    Returns:
        List of encoded features
    """
    features = []
    
    # Gender encoding (5-6)
    features.extend([
        1 if gender == "Female" else 0,  # Gender_Female
        1 if gender == "Male" else 0,    # Gender_Male
    ])
    
    # Marital status encoding (7-8)
    features.extend([
        1 if married == "No" else 0,     # Married_No
        1 if married == "Yes" else 0,    # Married_Yes
    ])
    
    # Dependents encoding (9-12)
    features.extend([
        1 if dependents == "0" else 0,      # Dependents_0
        1 if dependents == "1" else 0,      # Dependents_1
        1 if dependents == "2" else 0,      # Dependents_2
        1 if dependents == "3+" else 0,     # Dependents_3+
    ])
    
    # Education encoding (13-14)
    features.extend([
        1 if education == "Graduate" else 0,           # Education_Graduate
        1 if education == "Not Graduate" else 0,       # Education_Not Graduate
    ])
    
    # Employment encoding (15-16)
    features.extend([
        1 if self_employed == "No" else 0,      # Self_Employed_No
        1 if self_employed == "Yes" else 0,     # Self_Employed_Yes
    ])
    
    # Property area encoding (17-19)
    features.extend([
        1 if property_area == "Rural" else 0,       # Property_Area_Rural
        1 if property_area == "Semiurban" else 0,   # Property_Area_Semiurban
        1 if property_area == "Urban" else 0,       # Property_Area_Urban
    ])
    
    return features


def create_feature_vector(income: float, coapplicant_income: float, loan_amount: float,
                         loan_term: int, credit_history: int, categorical_features: list) -> pd.DataFrame:
    """
    Create a feature vector DataFrame with proper structure for model prediction.
    
    Args:
        income: Applicant's monthly income
        coapplicant_income: Co-applicant's monthly income
        loan_amount: Requested loan amount
        loan_term: Loan term in months
        credit_history: Credit history (1=Good, 0=Bad)
        categorical_features: List of encoded categorical features
        
    Returns:
        DataFrame with all features in correct format
    """
    # Build numeric features (0-4)
    features_list = [
        income,
        coapplicant_income,
        loan_amount,
        loan_term,
        credit_history,
    ]
    
    # Add categorical features (5-19)
    features_list.extend(categorical_features)
    
    # Create DataFrame with proper column names
    features_df = pd.DataFrame([features_list], columns=FEATURE_NAMES)
    
    return features_df


def apply_business_rules(model_prediction: str, model_probability: np.ndarray,
                        income: float, coapplicant_income: float, loan_amount: float,
                        loan_term: int, credit_history: int) -> Tuple[str, str, Dict[str, float]]:
    """
    Apply business logic rules to override or validate model predictions.
    
    Args:
        model_prediction: Raw model prediction ('Y' or 'N')
        model_probability: Model prediction probabilities
        income: Applicant's monthly income
        coapplicant_income: Co-applicant's monthly income
        loan_amount: Requested loan amount
        loan_term: Loan term in months
        credit_history: Credit history (1=Good, 0=Bad)
        
    Returns:
        Tuple of (final_prediction, rejection_reason, metrics_dict)
    """
    total_income = income + coapplicant_income
    final_prediction = model_prediction
    rejection_reason = ""
    metrics = {
        'total_income': total_income,
        'loan_to_income': 0,
        'monthly_emi': 0,
    }
    
    # Rule 0: Edge cases - Zero values
    if total_income == 0:
        final_prediction = 'N'
        rejection_reason = "Applicant has zero income"
    elif loan_amount == 0:
        final_prediction = 'N'
        rejection_reason = "Loan amount cannot be zero"
    
    # Rule 1: Bad credit history
    elif credit_history == 0:
        final_prediction = 'N'
        rejection_reason = "Bad/No credit history"
    
    # Rule 2 & 3: Income-based checks
    elif total_income > 0:
        monthly_emi = loan_amount / loan_term
        loan_to_income = monthly_emi / total_income
        metrics['monthly_emi'] = monthly_emi
        metrics['loan_to_income'] = loan_to_income
        
        # High loan-to-income ratio
        if loan_to_income > BUSINESS_RULES['max_loan_to_income_ratio'] and final_prediction == 'Y':
            final_prediction = 'N'
            rejection_reason = f"Loan-to-Income ratio too high ({loan_to_income:.2f})"
        
        # Low income for high loan
        elif total_income < BUSINESS_RULES['min_income_for_high_loan'] and \
             loan_amount > BUSINESS_RULES['high_loan_threshold']:
            final_prediction = 'N'
            rejection_reason = "Income too low for requested loan amount"
    
    return final_prediction, rejection_reason, metrics


def display_application_summary(gender: str, married: str, dependents: str,
                               education: str, self_employed: str, income: float,
                               coapplicant_income: float, loan_amount: float,
                               loan_term: int, property_area: str, credit_history: int) -> None:
    """Display a formatted summary of the application details."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📋 Personal Information:**")
        st.write(f"  • Gender: {gender}")
        st.write(f"  • Marital Status: {married}")
        st.write(f"  • Dependents: {dependents}")
        st.write(f"  • Education: {education}")
        st.write(f"  • Employment: {'Self-Employed' if self_employed == 'Yes' else 'Regular Employee'}")
    
    with col2:
        st.write("**💰 Financial Details:**")
        st.write(f"  • Income: ₹{income:,.0f}")
        st.write(f"  • Co-applicant Income: ₹{coapplicant_income:,.0f}")
        st.write(f"  • Total Income: ₹{income + coapplicant_income:,.0f}")
        st.write(f"  • Loan Amount: ₹{loan_amount:,.0f}")
        st.write(f"  • Loan Term: {loan_term} months")
        st.write(f"  • Property Area: {property_area}")
        st.write(f"  • Credit History: {'Good' if credit_history == 1 else 'Bad/None'}")


# ============================================================================
# MAIN APP INTERFACE
# ============================================================================

def main():
    """Main application function."""
    
    # Page header
    st.title("🏦 Loan Approval Prediction App")
    st.markdown("---")
    
    # Introduction
    st.markdown("""
    ### About This App
    This professional machine learning application predicts whether a bank loan application 
    will be **approved or rejected** based on applicant information using a trained 
    **Logistic Regression model**.
    
    **Key Features:**
    - 💡 Intelligent predictions backed by ML
    - ✅ Business logic validation rules
    - 📊 Real-time confidence scores
    - 🔍 Transparent decision explanations
    """)
    
    st.markdown("---")
    
    # Try to load model
    try:
        model = load_model()
    except Exception as e:
        st.error(f"❌ **Critical Error:** Could not load the model file.\n\n{str(e)}")
        st.info("💡 **Troubleshooting:** Ensure `model.pkl` exists in the application directory.")
        st.stop()
    
    # Input form
    st.header("📝 Application Details")
    
    col1, col2 = st.columns(2)
    
    # ===== PERSONAL INFORMATION =====
    with col1:
        st.subheader("📋 Personal Information")
        
        gender = st.selectbox(
            "Gender",
            ["Male", "Female"],
            help="Applicant's gender"
        )
        
        married = st.selectbox(
            "Marital Status",
            ["No", "Yes"],
            help="Is the applicant married?"
        )
        
        dependents = st.selectbox(
            "Number of Dependents",
            ["0", "1", "2", "3+"],
            help="Number of dependents (including spouse and children)"
        )
        
        education = st.selectbox(
            "Education Level",
            ["Graduate", "Not Graduate"],
            help="Highest education level achieved"
        )
        
        self_employed = st.selectbox(
            "Employment Type",
            ["No", "Yes"],
            help="Is the applicant self-employed? (No = Salaried Employee)"
        )
    
    # ===== FINANCIAL INFORMATION =====
    with col2:
        st.subheader("💰 Financial Information")
        
        income = st.number_input(
            "Applicant Income (Monthly, in currency units)",
            min_value=0,
            max_value=1000000,
            value=5000,
            step=100,
            help="Monthly salary of the applicant (Typical: ₹2,000 - ₹50,000)"
        )
        
        coapplicant_income = st.number_input(
            "Co-applicant Income (Monthly, in currency units)",
            min_value=0,
            max_value=1000000,
            value=0,
            step=100,
            help="Monthly salary of co-applicant if applicable (Spouse, Parent, etc.)"
        )
        
        loan_amount = st.number_input(
            "Loan Amount (in currency units)",
            min_value=0,
            max_value=1000000,
            value=100000,
            step=1000,
            help="Total loan amount requested (Typical: ₹50,000 - ₹500,000)"
        )
        
        loan_term = st.selectbox(
            "Loan Amount Term (Months)",
            [60, 120, 180, 240, 360],
            index=4,
            help="Duration of the loan (5yr, 10yr, 15yr, 20yr, 30yr)"
        )
    
    # ===== CREDIT & PROPERTY =====
    st.markdown("---")
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("📊 Credit Information")
        credit_history = st.selectbox(
            "Credit History",
            [1, 0],
            format_func=lambda x: "✅ Good (1)" if x == 1 else "❌ Bad/No History (0)",
            help="Does the applicant have a good credit history? (Critical for approval)"
        )
    
    with col4:
        st.subheader("🏠 Property Details")
        property_area = st.selectbox(
            "Property Area",
            ["Urban", "Semiurban", "Rural"],
            help="Type of area where the property is located"
        )
    
    st.markdown("---")
    
    # ===== PREDICTION BUTTON =====
    col_button = st.columns([1, 1, 1])
    with col_button[1]:
        predict_button = st.button(
            "🔮 Predict Loan Status",
            use_container_width=True,
            type="primary"
        )
    
    # ===== PREDICTION LOGIC =====
    if predict_button:
        # Validate inputs
        is_valid, error_msg = validate_inputs(income, coapplicant_income, loan_amount, loan_term)
        if not is_valid:
            st.error(error_msg)
        else:
            # Show loading state
            with st.spinner("🔄 Processing your application..."):
                try:
                    # Encode categorical features
                    cat_features = encode_categorical_features(
                        gender, married, dependents, education, self_employed, property_area
                    )
                    
                    # Create feature vector
                    features_df = create_feature_vector(
                        income, coapplicant_income, loan_amount, loan_term, 
                        credit_history, cat_features
                    )
                    
                    # Validate feature count
                    if features_df.shape[1] != model.n_features_in_:
                        st.error(
                            f"❌ Feature mismatch! Expected {model.n_features_in_} features, "
                            f"got {features_df.shape[1]}."
                        )
                        st.stop()
                    
                    # Make prediction
                    prediction = model.predict(features_df)
                    prediction_proba = model.predict_proba(features_df)
                    
                    # Apply business rules
                    final_prediction, rejection_reason, metrics = apply_business_rules(
                        prediction[0], prediction_proba[0], income, coapplicant_income,
                        loan_amount, loan_term, credit_history
                    )
                    
                except Exception as e:
                    st.error(f"❌ **Prediction Error:** {str(e)}")
                    logger.error(f"Prediction error: {e}")
                    st.info("💡 Please ensure all fields are filled correctly and try again.")
                    st.stop()
            
            # ===== DISPLAY RESULTS =====
            st.markdown("---")
            st.header("📊 Prediction Results")
            
            # Main prediction result
            result_col1, result_col2, result_col3 = st.columns([2, 1, 1])
            
            with result_col1:
                if final_prediction == 'Y':
                    st.success("✅ **LOAN APPROVED**", icon="✅")
                    st.markdown("*Congratulations! Your loan application has been approved.*")
                else:
                    st.error("❌ **LOAN REJECTED**", icon="❌")
                    st.markdown("*Unfortunately, your loan application has been rejected.*")
            
            # Display rejection reason if applicable
            if rejection_reason:
                st.warning(f"⚠️ **Reason:** {rejection_reason}", icon="⚠️")
            
            # Probabilities and confidence
            with result_col2:
                approval_prob = prediction_proba[0][1] * 100
                st.metric(
                    "Approval Probability",
                    f"{approval_prob:.1f}%",
                    delta=None
                )
            
            with result_col3:
                confidence = max(prediction_proba[0]) * 100
                st.metric(
                    "Model Confidence",
                    f"{confidence:.1f}%",
                    delta=None
                )
            
            rejection_prob = prediction_proba[0][0] * 100
            st.metric("Rejection Probability", f"{rejection_prob:.1f}%")
            
            # Advanced metrics
            st.markdown("---")
            st.subheader("📈 Financial Analysis")
            
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            
            with metrics_col1:
                st.metric(
                    "Total Income",
                    f"₹{metrics['total_income']:,.0f}/month",
                    help="Combined monthly income of applicant and co-applicant"
                )
            
            with metrics_col2:
                st.metric(
                    "Monthly EMI",
                    f"₹{metrics['monthly_emi']:,.0f}",
                    help="Estimated monthly loan payment"
                )
            
            with metrics_col3:
                st.metric(
                    "Loan-to-Income Ratio",
                    f"{metrics['loan_to_income']:.2f}x",
                    help=f"Monthly EMI as multiple of monthly income (Safe: <{BUSINESS_RULES['max_loan_to_income_ratio']}x)"
                )
            
            # Application summary
            st.markdown("---")
            st.subheader("📋 Application Summary")
            display_application_summary(
                gender, married, dependents, education, self_employed,
                income, coapplicant_income, loan_amount, loan_term,
                property_area, credit_history
            )
            
            # Debug information (hidden by default)
            with st.expander("🔍 Debug Information", expanded=False):
                st.write("**Feature Vector Details:**")
                st.write(f"  • Shape: {features_df.shape}")
                st.write(f"  • Expected Features: {model.n_features_in_}")
                st.write(f"  • Model Classes: {model.classes_}")
                st.json({
                    'model_prediction': prediction[0],
                    'model_probabilities': {
                        'rejection': float(prediction_proba[0][0]),
                        'approval': float(prediction_proba[0][1]),
                    },
                    'final_prediction': final_prediction,
                    'business_rules_applied': bool(rejection_reason),
                })
    
    # ===== FOOTER =====
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px; color: #666;">
    <small>
    📚 **Model Details:** Logistic Regression | 🎯 **Accuracy:** 78.47% | 
    🔐 **Privacy:** All data is processed locally<br>
    💡 **Disclaimer:** This prediction is for informational purposes only and 
    does not constitute financial advice.
    </small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
