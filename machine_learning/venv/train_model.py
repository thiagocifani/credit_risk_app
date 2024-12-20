import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Example updated data
data = {
    'income': [50000, 60000, 45000, 75000],
    'credit_score': [650, 700, 600, 750],
    'loan_amount': [20000, 25000, 30000, 10000],
    'expenses': [15000, 16000, 12000, 10000],
    'total_revolving_debt': [10000, 12000, 15000, 5000],
    'total_installment_balance': [5000, 6000, 8000, 3000],
    'risk_level': ['low_risk', 'low_risk', 'high_risk', 'low_risk']
}

# Load data into a pandas DataFrame
df = pd.DataFrame(data)

# Encode the target variable ('low_risk' -> 0, 'high_risk' -> 1)
df['risk_level'] = df['risk_level'].apply(lambda x: 1 if x == 'high_risk' else 0)

# Features and target variable
X = df[['income', 'credit_score', 'loan_amount', 'expenses', 'total_revolving_debt', 'total_installment_balance']]
y = df['risk_level']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, 'credit_risk_model.pkl')
print("Model trained and saved!")
