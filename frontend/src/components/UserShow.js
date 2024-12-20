import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const UserShow = () => {
  const { id } = useParams();
  const [user, setUser] = useState(null);
  const [limeData, setLimeData] = useState({});
  const [riskLevel, setRiskLevel] = useState("");

  useEffect(() => {
    const fetchUser = async () => {
      const res = await fetch(`http://localhost:3000/users/${id}`);
      const data = await res.json();
      setUser(data);

      const predictionRes = await fetch(
        `http://localhost:3000/users/${id}/credit_evaluations`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        },
      );
      const predictionData = await predictionRes.json();
      setRiskLevel(predictionData.predicted_risk_level);
      setLimeData(predictionData.lime_explanation);
    };
    fetchUser();
  }, [id]);

  if (!user || !limeData) return <div>Loading...</div>;

  const limeExplanationData = Object.keys(limeData).map((key) => ({
    name: key,
    value: limeData[key],
  }));

  console.log(limeExplanationData);

  return (
    <div className="user-show-wrapper">
      <div className="user-card">
        <h2 className="card-title">User Details</h2>
        <div className="card-content">
          <p>
            <strong>Name:</strong> {user.name}
          </p>
          <p>
            <strong>Email:</strong> {user.email}
          </p>
          <p>
            <strong>Income:</strong> ${user.income.toLocaleString()}
          </p>
          <p>
            <strong>Expenses:</strong> ${user.expenses.toLocaleString()}
          </p>
          <p>
            <strong>Credit Score:</strong> {user.credit_score}
          </p>
          <p>
            <strong>Total Revolving Debt:</strong> $
            {user.total_revolving_debt.toLocaleString()}
          </p>
          <p>
            <strong>Total Installment Balance:</strong> $
            {user.total_installment_balance.toLocaleString()}
          </p>
          <p>
            <strong>Loan Amount:</strong> ${user.loan_amount.toLocaleString()}
          </p>
          <p>
            <strong>Risk Level:</strong> {riskLevel}
          </p>
        </div>
      </div>

      <div className="chart-card">
        <h2 className="card-title">Risk Analysis</h2>
        <div className="chart-placeholder">
          {limeData && (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={limeExplanationData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#82ca9d" />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserShow;
