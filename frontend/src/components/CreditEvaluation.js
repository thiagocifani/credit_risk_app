import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const CreditRiskPrediction = () => {
  const [predictionData, setPredictionData] = useState(null);

  useEffect(() => {
    const fetchPredictionData = async () => {
      try {
        const response = await axios.post(
          "http://localhost:3000/users/1/credit_evaluations",
          {},
        );
        setPredictionData(response.data);
      } catch (error) {
        console.error("Error fetching prediction data:", error);
      }
    };

    fetchPredictionData();
  }, []);

  if (!predictionData) {
    return <div>Loading...</div>;
  }

  const { prediction, lime_explanation, feature_values } = predictionData;

  // Format data for LineChart
  const featureValuesData = Object.keys(feature_values).map((key) => ({
    name: key,
    value: feature_values[key],
  }));

  const limeExplanationData = Object.keys(lime_explanation).map((key) => ({
    name: key,
    value: lime_explanation[key],
  }));

  return (
    <div>
      <h2>Credit Risk Prediction: {prediction}</h2>

      {/* Feature Values LineChart */}
      <h3>Feature Values</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={featureValuesData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="value" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>

      {/* LIME Explanations LineChart */}
      <h3>LIME Explanations</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={limeExplanationData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="value" stroke="#82ca9d" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CreditRiskPrediction;
