# Interview Notes for This Project

Quick prep for when people ask about this project.

## The Elevator Pitch (30 seconds)

"I built a machine learning model that predicts loan approvals. Started with about 1000 loan applications - some approved, some rejected. I tested 4 different algorithms and found that Logistic Regression worked best, getting 78% accuracy. It looks at stuff like income, credit history, and loan amount to decide if a loan is likely to get approved or not."

Simple. Done.

## Common Questions

### "Why did you choose Logistic Regression?"

"I tested 4 different models and Logistic Regression got the best accuracy - 78.47%. But also, for this kind of banking problem, you want a model that's interpretable. You need to be able to explain WHY you're approving or rejecting someone's loan. Logistic Regression gives you that - you can see which factors matter most. Tree-based models are like black boxes."

### "How did you handle the missing data?"

"So about 55% of the credit history column was missing, which was a lot. If I just deleted those rows, I'd lose half my data. Instead, I filled in the missing values - categorical fields with the mode (most common value) and numerical fields with the mean. It's not perfect but it preserved the information better than deleting whole rows."

### "How do you know your model is actually good?"

"I used cross-validation - specifically Stratified K-Fold with 5 folds. That way I don't just test on one random split. I test on 5 different train/test combinations and average the results. That gives me a more honest picture of how the model will perform on new data. The results were consistent, so I'm confident the 78% is real and not just luck."

### "Which features were most important?"

"Credit history was by far the most important. People with good credit have like a 79% approval rate, and people without it have like 8%. That's a huge difference. Income also matters - higher income, better chances. And the loan-to-income ratio matters too - if you're asking for a huge loan relative to your income, you're gonna get rejected."

### "What was the hardest part?"

"Probably the missing data. The naive solution is to just delete rows with missing values, but that would've thrown away a lot of data. Had to think about how to handle it without introducing too much bias. And also making sure cross-validation was set up correctly so I wasn't accidentally leaking information from test into training data."

### "Did you try any other approaches?"

"Yeah, I tested 4 different algorithms instead of just going with one. Logistic Regression, Random Forest, XGBoost, and Decision Tree. The first three were pretty close (77-78%), but Decision Tree did worse with 64%. If I had more time, I'd probably try ensemble methods or hyperparameter tuning, but these results were already pretty good."

## Things I'd Change If I Did It Again

- Probably would've tried more feature engineering. Maybe create some custom features from the existing ones.
- Could've explored ensemble methods more
- Would be cool to integrate real credit bureau data instead of just the flags in the dataset
- Should've saved more intermediate results/visualizations during the process

## If They Ask About Production

"For production, I'd probably wrap this in a Flask API. Banks could call it with applicant data (income, credit history, etc.) and get back a prediction. It would be pretty fast - sub-100ms response times. You'd also want monitoring to track if the model's performance dips over time, which could happen if loan patterns change."

## Keywords to Remember

- 78.47% accuracy
- 981 applications (614 train, 367 test)
- Cross-validation / Stratified K-Fold
- Credit history was most important feature
- Logistic Regression beat the other 3 models
- Data had significant missing values
- scikit-learn, pandas, numpy

## If They Ask Technical Questions

**Q: What's Stratified K-Fold?**  
A: "It makes sure each train/test split has roughly the same distribution as the original data. Normal cross-validation might accidentally create a fold with 90% approved and 10% rejected, which would skew your results. Stratified keeps the splits balanced."

**Q: How do you evaluate a classification model?**  
A: "Accuracy is just the starting point. I also look at precision (of the people I predict will be approved, how many actually are), recall (how many actual approvable loans do I find), and F1-score (balance of both). And ROC-AUC to see how well the model ranks people."

**Q: Why not just use accuracy?**  
A: "Accuracy can be misleading. If 80% of loans get approved, a model that just says 'approve everything' would get 80% accuracy but would be useless. You need to look at precision and recall to see if it's actually good."

## Don't Say

- "I'm not sure how this works" (you built it, own it)
- "AI did this for me" (that's sus)
- "Let me look at the code" (have it ready so you can reference it)
- Talk down about your own work

## Do Say

- "This is what I tried..."
- "Here's why I chose this approach..."
- "If I had more time, I would..."
- "The main challenge was..."
