# Project Summary - Quick Version

## What I Did

Built a machine learning model to predict loan approvals. 

**In 30 seconds:**
"I trained a model on 981 loan applications using 4 different algorithms. Logistic Regression came out on top with 78.47% accuracy. It learns from factors like income, credit history, and loan amount to predict if a bank should approve or reject a loan."

## Numbers That Matter

- **Accuracy:** 78.47% (got 78 out of 100 right)
- **Training data:** 614 applications
- **Test data:** 367 applications
- **Features used:** 12 (income, credit, employment, etc.)
- **Models tested:** 4 (LR won)

## The Interesting Part

**Credit history is THE most important thing** - people with good credit get approved 79.5% of the time. Without it? Only 8.2%. That's a huge difference.

Income also matters a lot. But it's not just about having high income - it's about the loan-to-income ratio. Asking for a $500k loan on a $50k salary = rejected.

## Technical Stuff

- Used scikit-learn for ML
- pandas for data work
- matplotlib for plotting
- Stratified K-Fold cross-validation (to keep results honest)
- Tested: Logistic Regression, Random Forest, XGBoost, Decision Tree

## Why Logistic Regression?

1. Best accuracy (78.47%)
2. Fast (real-time predictions)
3. Explainable (can see WHY it approves/rejects)
4. Simple (easy to deploy)

## Files

- `loan-approval-prediction.ipynb` - All the code
- `train_*.csv` - Training data
- `test_*.csv` - Test data

## How to Run

```bash
pip install pandas numpy matplotlib seaborn scikit-learn xgboost jupyter
jupyter notebook loan-approval-prediction.ipynb
```

Then run all cells. Takes about 5 minutes.

## What You'll Learn

- How to clean messy data
- How to compare different ML models
- How to evaluate if a model is actually good
- Real-world machine learning workflow

That's it!
