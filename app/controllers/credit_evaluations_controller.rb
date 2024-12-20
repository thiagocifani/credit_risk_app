require "httparty"

class CreditEvaluationsController < ApplicationController
  require "net/http"
  require "uri"
  require "json"

  def create
    uri = URI.parse("http://localhost:5000/predict")  # Flask app URL

    user = User.find(params[:user_id])

    data = {
      income: user.income,
      expenses: user.expenses,
      credit_score: user.credit_score,
      loan_amount: user.loan_amount,
      total_revolving_debt: user.total_revolving_debt,
      total_installment_balance: user.total_installment_balance

    }

    # Send data to Flask app via POST request
    response = Net::HTTP.post(uri, data.to_json, "Content-Type" => "application/json")

    # Parse Flask response
    result = JSON.parse(response.body)

    # Return the result to React frontend
    render json: result, status: 200, content_type: "application/json; charset=utf-8"
  end
end
