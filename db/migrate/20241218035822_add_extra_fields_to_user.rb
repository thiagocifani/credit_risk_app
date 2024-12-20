class AddExtraFieldsToUser < ActiveRecord::Migration[7.2]
  def change
    add_column :users, :loan_amount, :decimal
    add_column :users, :total_revolving_debt, :decimal
    add_column :users, :total_installment_balance, :decimal
  end
end
