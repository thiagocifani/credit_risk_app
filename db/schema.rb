# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.2].define(version: 2024_12_18_035822) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "credit_evaluations", force: :cascade do |t|
    t.bigint "user_id", null: false
    t.decimal "risk_score"
    t.string "risk_category"
    t.jsonb "explanation"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["user_id"], name: "index_credit_evaluations_on_user_id"
  end

  create_table "users", force: :cascade do |t|
    t.string "name"
    t.string "email"
    t.decimal "income"
    t.decimal "expenses"
    t.integer "credit_score"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.decimal "loan_amount"
    t.decimal "total_revolving_debt"
    t.decimal "total_installment_balance"
  end

  add_foreign_key "credit_evaluations", "users"
end
