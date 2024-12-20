class CreateUsers < ActiveRecord::Migration[7.2]
  def change
    create_table :users do |t|
      t.string :name
      t.string :email
      t.decimal :income
      t.decimal :expenses
      t.integer :credit_score

      t.timestamps
    end
  end
end
