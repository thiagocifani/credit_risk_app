import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const CreateUser = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    income: "",
    expenses: "",
    credit_score: "",
    total_revolving_debt: "",
    total_installment_balance: "",
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch("http://localhost:3000/users", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    if (response.ok) {
      navigate("/");
    } else {
      alert("Failed to create user");
    }
  };

  return (
    <div className="create-user-container">
      <h1>Create User</h1>
      <form className="create-user-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Name</label>
          <input
            id="name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="income">Income</label>
          <input
            type="number"
            id="income"
            name="income"
            value={formData.income}
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="expenses">Expenses</label>
          <input
            type="number"
            id="expenses"
            name="expenses"
            value={formData.expenses}
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="credit_score">Credit Score</label>
          <input
            type="number"
            id="credit_score"
            name="credit_score"
            value={formData.credit_score}
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="loan_amount">Loan Amount</label>
          <input
            type="number"
            id="loan_amount"
            name="loan_amount"
            value={formData.loan_amount}
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="total_revolving_debt">Total Revolving Debt</label>
          <input
            type="number"
            id="total_revolving_debt"
            name="total_revolving_debt"
            value={formData.total_revolving_debt}
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="total_installment_balance">
            Total Installment Balance
          </label>
          <input
            type="number"
            id="total_installment_balance"
            name="total_installment_balance"
            value={formData.total_installment_balance}
            onChange={handleInputChange}
            required
          />
        </div>

        <button type="submit" className="submit-button">
          Create User
        </button>
      </form>
    </div>
  );
};

export default CreateUser;
