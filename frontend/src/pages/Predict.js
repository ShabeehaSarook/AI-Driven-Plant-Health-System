import React, { useState } from "react";
import { predictPlantHealth } from "../services/api";

const Predict = () => {
  const [formData, setFormData] = useState({
    Plant_ID: 1,
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
  const [error, setError] = useState("");

  // -----------------------------
  // HANDLE INPUT CHANGE
  // -----------------------------
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // -----------------------------
  // SUBMIT FORM
  // -----------------------------
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await predictPlantHealth(formData);
      setResult(response);
    } catch (err) {
      setError("❌ Failed to connect to AI server");
    }
  };

  // -----------------------------
  // STATUS COLOR
  // -----------------------------
  const getStatusColor = (status) => {
    if (status === "Healthy") return "green";
    if (status === "Moderate Stress") return "orange";
    if (status === "High Stress") return "red";
    return "black";
  };

  return (
    <div style={{ padding: "20px", maxWidth: "700px" }}>
      <h2>🌱 Plant Health Prediction</h2>

      {/* ---------------- FORM ---------------- */}
      <form onSubmit={handleSubmit}>
        {Object.keys(formData).map((key) => (
          <div key={key} style={{ marginBottom: "8px" }}>
            <label>{key}</label>
            <input
              type="number"
              name={key}
              value={formData[key]}
              onChange={handleChange}
              required
              min="0"
              style={{ width: "100%" }}
            />
          </div>
        ))}

        <button type="submit" style={{ marginTop: "10px" }}>
          Predict
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* ---------------- RESULT ---------------- */}
      {result && (
        <div style={{ marginTop: "25px" }}>
          <h3>🧠 Prediction Result</h3>

          {/* STATUS */}
          <p
            style={{
              color: getStatusColor(result.prediction),
              fontWeight: "bold",
              fontSize: "18px"
            }}
          >
            🔴 Status: {result.prediction}
          </p>

          {/* CONFIDENCE */}
          <p><strong>Confidence:</strong> {result.confidence}</p>

          {/* CONFIDENCE BAR */}
          <div
            style={{
              background: "#eee",
              borderRadius: "20px",
              overflow: "hidden",
              height: "22px",
              marginBottom: "15px"
            }}
          >
            <div
              style={{
                width: result.confidence,
                background: getStatusColor(result.prediction),
                height: "100%",
                color: "white",
                textAlign: "center"
              }}
            >
              {result.confidence}
            </div>
          </div>

          {/* EXPLANATION */}
          <h4>🔍 Explanation</h4>
          <ul>
            {result.explanation.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>

          {/* PLANT MESSAGE */}
          {result.plant_message && (
            <>
              <h4>💬 Plant Says</h4>
              <p>{result.plant_message.plant_message}</p>
            </>
          )}

          {/* DOWNLOAD REPORT */}
          {result.report && (
            <a
              href={`http://127.0.0.1:5000${result.report}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              <button style={{ marginTop: "15px" }}>
                📄 Download Health Report (PDF)
              </button>
            </a>
          )}
        </div>
      )}
    </div>
  );
};

export default Predict;
