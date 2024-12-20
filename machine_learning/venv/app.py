import lime
import lime.lime_tabular
import joblib
import numpy as np
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model = joblib.load('credit_risk_model.pkl')

# Load or create the training data for LIME explanation
train_data = np.array([
    [50000, 650, 20000, 5000, 3000, 7000],
    [60000, 700, 25000, 7000, 4000, 8000],
    [80000, 750, 30000, 8000, 5000, 12000],
    [90000, 800, 40000, 9000, 6000, 15000],
    [30000, 600, 15000, 4000, 1500, 5000],
    [40000, 580, 17000, 4500, 2500, 6500]
])

train_labels = [0, 1, 1, 1, 0, 0]  # Low risk (0), High risk (1)

# Create a LIME explainer for tabular data
explainer = lime.lime_tabular.LimeTabularExplainer(
    train_data, training_labels=train_labels, mode="classification",
    feature_names=["income", "credit_score", "loan_amount", "expenses", "total_revolving_debt", "total_installment_balance"]
)

@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from the request
    data = request.get_json()

    # Extract features from the request data, ensuring they are numeric
    income = float(data.get('income'))
    credit_score = float(data.get('credit_score'))
    loan_amount = float(data.get('loan_amount'))
    expenses = float(data.get('expenses'))
    total_revolving_debt = float(data.get('total_revolving_debt'))
    total_installment_balance = float(data.get('total_installment_balance'))

    # Prepare data for prediction (convert to numpy array)
    input_data = np.array([[income, credit_score, loan_amount, expenses, total_revolving_debt, total_installment_balance]])

    # Predict risk level
    prediction = model.predict(input_data)

    # Generate LIME explanation for this prediction
    explanation = explainer.explain_instance(input_data[0], model.predict_proba)

    # Map the prediction to "high_risk" or "low_risk"
    risk = 'high_risk' if prediction[0] == 1 else 'low_risk'   # Prepare LIME explanation (feature contributions) and convert numpy types to native Python types

    lime_explanation = {
        f"Feature {i}": float(explanation.local_exp[1][i][0])  # Using explanation.local_exp[1] for the feature contributions for class 1
        for i in range(len(input_data[0]))
    }

    chart_data = {
        "prediction": risk,
        "feature_values": {
            "income": income,
            "credit_score": credit_score,
            "loan_amount": loan_amount,
            "expenses": expenses,
            "total_revolving_debt": total_revolving_debt,
            "total_installment_balance": total_installment_balance,
        },
        "lime_explanation": lime_explanation
    }

    # Convert all int64/float64 types to native Python types using item()
    chart_data = {key: (value.item() if isinstance(value, np.generic) else value) for key, value in chart_data.items()}

    return jsonify(chart_data)

if __name__ == '__main__':
    app.run(debug=True)

