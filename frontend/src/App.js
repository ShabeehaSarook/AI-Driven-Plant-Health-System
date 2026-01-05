import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    Plant_ID: "",
    Soil_Moisture: "",
    Ambient_Temperature: "",
    Soil_Temperature: "",
    Humidity: "",
    Light_Intensity: "",
    Soil_pH: "",
    Nitrogen_Level: "",
    Phosphorus_Level: "",
    Potassium_Level: "",
    Chlorophyll_Content: "",
    Electrochemical_Signal: ""
  });

  const [result, setResult] = useState(null);

  // -------------------------------
  // UI HELPERS
  // -------------------------------
  const getStatusColor = (status) => {
    if (status === "Healthy") return "green";
    if (status === "Moderate Stress") return "orange";
    if (status === "High Stress") return "red";
    return "black";
  };

  const getStatusIcon = (status) => {
    if (status === "Healthy") return "🟢";
    if (status === "Moderate Stress") return "🟡";
    if (status === "High Stress") return "🔴";
    return "🌱";
  };

  // -------------------------------
  // VALIDATION
  // -------------------------------
  const validateInput = () => {
    for (const key in formData) {
      if (formData[key] === "" || isNaN(formData[key])) {
        alert(`Please enter a valid value for ${key}`);
        return false;
      }
      if (Number(formData[key]) < 0) {
        alert(`${key} cannot be negative`);
        return false;
      }
    }
    return true;
  };

  // -------------------------------
  // HANDLERS
  // -------------------------------
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateInput()) return;

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/predict",
        formData
      );
      setResult(response.data);
    } catch (error) {
      alert("Backend server error. Please check Flask is running.");
    }
  };

  // -------------------------------
  // UI
  // -------------------------------
  return (
    <div className="container">
      <h1>🌱 Plant Health Prediction</h1>

      <form onSubmit={handleSubmit}>
        {Object.keys(formData).map((key) => (
          <div key={key}>
            <label>{key}</label>
            <input
              type="number"
              name={key}
              value={formData[key]}
              onChange={handleChange}
            />
          </div>
        ))}
        <button type="submit">Predict</button>
      </form>

      {result && (
        <div className="result">
          <h2>🧠 Prediction Result</h2>

          <h3 style={{ color: getStatusColor(result.prediction) }}>
            {getStatusIcon(result.prediction)} Status: {result.prediction}
          </h3>

          <p><strong>Confidence:</strong> {result.confidence}</p>

          {/* Confidence Progress Bar */}
          <div className="progress">
            <div
              className="progress-bar"
              style={{
                width: result.confidence,
                background: getStatusColor(result.prediction)
              }}
            >
              {result.confidence}
            </div>
          </div>

          <h3>🔍 Explanation</h3>
          <ul>
            {result.explanation.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>

          {result.plant_message && (
            <>
              <h3>💬 Plant Says</h3>
              <p>{result.plant_message.plant_message}</p>
            </>
          )}

          {/* PDF REPORT DOWNLOAD */}
          {result.report && (
            <a
              href={`http://127.0.0.1:5000/${result.report}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              <button className="download-btn">
                📄 Download Health Report (PDF)
              </button>
            </a>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
