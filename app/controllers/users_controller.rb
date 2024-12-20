class UsersController < ApplicationController
  def index
    users = User.all
    render json: users
  end

  def show
    user = User.find(params[:id])
    render json: user
  end

  def create
    user = User.new(user_params)
    if user.save
      render json: user, status: :created
    else
      render json: {errors: user.errors.full_messages}, status: :unprocessable_entity
    end
  end

  private

  def user_params
    params.require(:user).permit(
      :name, :email, :income, :expenses, :credit_score,
      :loan_amount, :total_revolving_debt, :total_installment_balance
    )
  end
end
