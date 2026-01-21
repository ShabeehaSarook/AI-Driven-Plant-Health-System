import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "http://127.0.0.1:5000";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [isLogin, setIsLogin] = useState(true);
  const [authData, setAuthData] = useState({ email: "", password: "" });
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
  const [loading, setLoading] = useState(false);

  // -------------------------------
  // AUTHENTICATION HANDLERS
  // -------------------------------
  const handleAuthChange = (e) => {
    setAuthData({ ...authData, [e.target.name]: e.target.value });
  };

  const handleAuth = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const endpoint = isLogin ? "/login" : "/register";
      const response = await axios.post(`${API_URL}${endpoint}`, authData);
      const receivedToken = response.data.token;
      setToken(receivedToken);
      localStorage.setItem("token", receivedToken);
      alert(isLogin ? "Login successful!" : "Registration successful!");
      setAuthData({ email: "", password: "" });
    } catch (error) {
      alert(error.response?.data?.error || "Authentication failed!");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setToken("");
    localStorage.removeItem("token");
    setResult(null);
    alert("Logged out successfully!");
  };

  // -------------------------------
  // PREDICTION HANDLERS
  // -------------------------------
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const validateInput = () => {
    for (let key in formData) {
      if (formData[key] === "") {
        alert(`Please fill in ${key}`);
        return false;
      }
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateInput()) return;

    setLoading(true);
    try {
      const response = await axios.post(
        `${API_URL}/predict`,
        formData,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      setResult(response.data);
    } catch (error) {
      alert(error.response?.data?.error || "Prediction failed! Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    if (status === "Healthy") return "green";
    if (status === "Moderate Stress") return "orange";
    if (status === "High Stress") return "red";
    return "black";
  };

  // -------------------------------
  // RENDER: LOGIN/REGISTER SCREEN
  // -------------------------------
  if (!token) {
    return (
      <div className="container">
        <h1>🌱 Plant Health Monitoring System</h1>
        <div className="auth-container">
          <h2>{isLogin ? "Login" : "Register"}</h2>
          <form onSubmit={handleAuth}>
            <div>
              <label>Email:</label>
              <input
                type="email"
                name="email"
                value={authData.email}
                onChange={handleAuthChange}
                required
                placeholder="your@email.com"
              />
            </div>
            <div>
              <label>Password:</label>
              <input
                type="password"
                name="password"
                value={authData.password}
                onChange={handleAuthChange}
                required
                placeholder="Min 8 characters"
              />
            </div>
            <button type="submit" disabled={loading}>
              {loading ? "Processing..." : (isLogin ? "Login" : "Register")}
            </button>
          </form>
          <p>
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <button
              className="link-button"
              onClick={() => setIsLogin(!isLogin)}
            >
              {isLogin ? "Register here" : "Login here"}
            </button>
          </p>
        </div>
      </div>
    );
  }

  // -------------------------------
  // RENDER: PREDICTION SCREEN
  // -------------------------------
  return (
    <div className="container">
      <div className="header">
        <h1>🌱 Plant Health Prediction</h1>
        <button onClick={handleLogout} className="logout-btn">
          Logout
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        {Object.keys(formData).map((key) => (
          <div key={key} className="form-group">
            <label>{key.replace(/_/g, " ")}:</label>
            <input
              type="number"
              step="any"
              name={key}
              value={formData[key]}
              onChange={handleChange}
              placeholder={`Enter ${key.replace(/_/g, " ")}`}
            />
          </div>
        ))}
        <button type="submit" className="predict-btn" disabled={loading}>
          {loading ? "Analyzing..." : "🔍 Predict Plant Health"}
        </button>
      </form>

      {result && (
        <div className="result-container">
          <h2>🌿 Prediction Results</h2>
          
          <div className="result-card">
            <h3>Health Status</h3>
            <p style={{ color: getStatusColor(result.prediction), fontSize: "24px", fontWeight: "bold" }}>
              {result.prediction}
            </p>
          </div>

          <div className="result-card">
            <h3>Confidence Score</h3>
            <p style={{ fontSize: "20px" }}>{result.confidence}</p>
          </div>

          {result.explanation && result.explanation.length > 0 && (
            <div className="result-card">
              <h3>📋 Key Factors</h3>
              <ul>
                {result.explanation.map((reason, index) => (
                  <li key={index}>{reason}</li>
                ))}
              </ul>
            </div>
          )}

          {result.plant_message && (
            <div className="result-card">
              <h3>💬 Plant Says</h3>
              <p>{result.plant_message.plant_message}</p>
            </div>
          )}

          {result.report && (
            <div className="result-card">
              <h3>📄 Report</h3>
              <a
                href={`${API_URL}${result.report}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                <button className="download-btn">
                  📥 Download Health Report (PDF)
                </button>
              </a>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
