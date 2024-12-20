from flask import Flask, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
from lime.lime_tabular import LimeTabularExplainer

app = Flask(__name__)

# Load CSV data
CSV_FILE = "credit_risk_data.csv"
data = pd.read_csv(CSV_FILE)

# Explicitly define all labels
all_classes = ['Low', 'Medium', 'High']

# Encode the target variable
label_encoder = LabelEncoder()
label_encoder.fit(all_classes)
data['risk_level_encoded'] = label_encoder.transform(data['risk_level'])

# Features and target
FEATURE_NAMES = ['income', 'expenses', 'credit_score', 'loan_amount', 'total_revolving_debt', 'total_installment_balance']
TARGET_NAME = 'risk_level_encoded'

X = data[FEATURE_NAMES]
y = data[TARGET_NAME]

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

#Load or create the training data for LIME explanation

train_data = np.array([
    [100000, 5000, 720, 0, 3000, 7000],
    [70000, 60000, 600, 20000, 10000, 20000],
    [50000, 70000, 500, 40000, 8000, 7000],

])

train_labels = [0, 1, 2]  # Low risk (0), High risk (1)

# Create a LIME explainer for tabular data
explainer = LimeTabularExplainer(
    train_data, training_labels=train_labels, mode="classification",
    class_names=all_classes)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Flask API endpoint to predict risk level and generate LIME explanation.
    """
    input_data = request.json

    # Convert input data to a DataFrame
    input_df = pd.DataFrame([input_data])

    # Ensure all numeric columns are properly converted
    for col in FEATURE_NAMES:
        input_df[col] = pd.to_numeric(input_df[col], errors='coerce')

    # Check for missing or invalid data
    if input_df.isnull().values.any():
        return jsonify({"error": "Invalid input data. Ensure all values are numeric."}), 400

    # Predict the risk level
    prediction = model.predict(input_df)
    decoded_label = label_encoder.inverse_transform(prediction)[0]

    # Generate LIME explanation
    explanation = explainer.explain_instance(
        input_df.values[0],
        model.predict_proba,
        num_features=len(FEATURE_NAMES)
    )

    # Extract feature contributions
    lime_explanation = {
        feature: float(weight) for feature, weight in explanation.as_list()
    }

    response = {
        "predicted_risk_level": decoded_label,
        "input_data": input_data,
        "lime_explanation": lime_explanation
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
