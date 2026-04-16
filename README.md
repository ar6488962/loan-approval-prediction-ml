# Loan Approval Prediction Project

A machine learning project that predicts whether a bank should approve a loan application. Built using Python and scikit-learn.

**Best Model:** Logistic Regression - **78.47% Accuracy**

## What This Does

The model takes customer loan application data (income, credit history, loan amount, etc.) and predicts if the bank should approve or reject it. 

I trained it on 614 past loan applications and tested it on 367 new ones. It gets about 78% right, which is pretty good.

## Files

- `loan-approval-prediction.ipynb` - Main notebook with all the code
- `train_u6lujuX_CVtuZ9i.csv` - Training data
- `test_Y3wMUE5_7gLdaTN.csv` - Test data

## How I Built It

1. **Data Cleaning** - The data had some missing values, so I filled them in. Used mode for text fields, mean for numbers.

2. **Explored the Data** - Looked at charts and patterns. Found that credit history is super important - people with good credit get approved 80% of the time.

3. **Built 4 Models**
   - Logistic Regression ← **Winner (78.47%)**
   - Random Forest (77.78%)
   - XGBoost (77.78%)
   - Decision Tree (64.58%)

4. **Tested Them** - Used cross-validation to make sure the accuracy is real and not just lucky

## Results

| Model | Accuracy |
|-------|----------|
| Logistic Regression | 78.47% |
| Random Forest | 77.78% |
| XGBoost | 77.78% |
| Decision Tree | 64.58% |

Logistic Regression won because it was most accurate and it's simple/fast for predictions.

## Key Findings

- **Credit history is huge** - Applicants with good credit: 79.5% approval vs 8.2% without
- **Income matters** - Higher income = easier approval
- **Loan amount/income ratio** - Requesting a huge loan relative to income gets you rejected
- **Location** - Urban areas approve slightly more than rural

## How to Run It

```bash
# Install requirements
pip install pandas numpy matplotlib seaborn scikit-learn xgboost jupyter

# Run the notebook
jupyter notebook loan-approval-prediction.ipynb

# Or run everything at once
jupyter nbconvert --to notebook --execute loan-approval-prediction.ipynb
```

## What You'll See

When you run the notebook, you get:
- Data exploration with plots
- Model comparisons
- Predictions on test data
- Visualization files saved

Total runtime: ~5 minutes

## Skills Used

- Python (pandas, scikit-learn, matplotlib)
- Machine learning (classification, cross-validation)
- Data preprocessing
- Model evaluation

