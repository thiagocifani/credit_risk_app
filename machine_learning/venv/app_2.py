from flask import Flask, request, jsonify
import xgboost as xgb
import lime.lime_tabular
import numpy as np
import pandas as pd
import joblib

app = Flask(__name__)

# Load the dataset and train the model
def train_model(csv_path='credit_risk_data.csv'):
    data = pd.read_csv(csv_path)
    X = data[['income', 'expenses', 'credit_score', 'total_revolving_debt', 'total_installment_balance', 'loan_amount']]
    y = data['credit_risk']

    # Train the model
    model = xgb.XGBClassifier()
    model.fit(X, y)

    # Save the model
    joblib.dump(model, 'credit_risk_model.pkl')

    # Initialize the LIME explainer
    explainer = lime.lime_tabular.LimeTabularExplainer(
        X.values, training_labels=y.values, mode="classification", feature_names=X.columns
    )
    return model, explainer

# Initial training
model, explainer = train_model()

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_data = np.array([[data.get('income'), data.get('expenses'), data.get('credit_score'), data.get('total_revolving_debt'), data.get('loan_amount'), data.get('total_installment_balance')]])
    prediction = model.predict(input_data)[0]
    prediction_proba = model.predict_proba(input_data)[0]

    # Explain with LIME
    explanation = explainer.explain_instance(input_data[0], model.predict_proba)
    lime_explanation = {f"Feature {i}": float(explanation.local_exp[0][i]) for i in range(input_data.shape[1])}

    response_data = {
        'prediction': int(prediction),
        'prediction_proba': prediction_proba.tolist(),
        'lime_explanation': lime_explanation
    }
    return jsonify(response_data)

@app.route('/api/train', methods=['POST'])
def train():
    csv_file = request.files['file']
    csv_file.save('credit_risk_data.csv')
    global model, explainer
    model, explainer = train_model('credit_risk_data.csv')
    return jsonify({"message": "Model retrained successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)

