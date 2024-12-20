class CreateCreditEvaluations < ActiveRecord::Migration[7.2]
  def change
    create_table :credit_evaluations do |t|
      t.references :user, null: false, foreign_key: true
      t.decimal :risk_score
      t.string :risk_category
      t.jsonb :explanation

      t.timestamps
    end
  end
end
