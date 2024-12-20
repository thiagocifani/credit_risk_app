import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load CSV data
data = pd.read_csv("credit_risk_data.csv")

# Encode risk_level as a target variable
all_classes = ['Low', 'Medium', 'High']

label_encoder = LabelEncoder()
label_encoder.fit(all_classes)
data['risk_level_encoded'] = label_encoder.fit_transform(data['risk_level'])

# Features and target
FEATURE_NAMES = ['income', 'expenses', 'credit_score', 'loan_amount',
                 'total_revolving_debt', 'total_installment_balance']

TARGET_NAME = 'risk_level_encoded'

X = data[FEATURE_NAMES]
y = data[TARGET_NAME]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)

# Prediction function
def predict_risk(input_data):
    """
    Predict risk level from input data.
    :param input_data: dict with keys as feature names and values as user inputs.
    :return: dict with predicted risk level and feature importance.
    """
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)
    risk_level = label_encoder.inverse_transform(prediction)[0]

    # Feature importance explanation
    feature_importances = {FEATURE_NAMES[i]: model.feature_importances_[i] for i in range(len(FEATURE_NAMES))}

    return {
        "predicted_risk_level": risk_level,
        "feature_importances": feature_importances,
        "input_data": input_data
    }

# Example Prediction
user_input = {
    "income": 55000,
    "expenses": 20000,
    "credit_score": 720,
    "loan_amount": 15000,
    "total_revolving_debt": 5000,
    "total_installment_balance": 10000
}

prediction_result = predict_risk(user_input)
print("Prediction Result:")
print(json.dumps(prediction_result, indent=4))

