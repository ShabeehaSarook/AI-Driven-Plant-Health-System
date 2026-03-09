import React, { useMemo, useState } from "react";
import { predictPlantHealth } from "../services/api";

import { downloadFile } from "../utils/download";

// Client-side validation rules (basic, adjustable).
// These ranges are practical defaults for UX validation.
const FIELD_RULES = {
  Plant_ID: { label: "Plant ID", min: 1, max: 9999, step: 1 },
  Soil_Moisture: { label: "Soil Moisture", min: 0, max: 100, step: 0.1, unit: "%" },
  Ambient_Temperature: { label: "Ambient Temperature", min: -10, max: 60, step: 0.1, unit: "°C" },
  Soil_Temperature: { label: "Soil Temperature", min: -5, max: 60, step: 0.1, unit: "°C" },
  Humidity: { label: "Humidity", min: 0, max: 100, step: 0.1, unit: "%" },
  Light_Intensity: { label: "Light Intensity", min: 0, max: 200000, step: 1, unit: "lux" },
  Soil_pH: { label: "Soil pH", min: 0, max: 14, step: 0.1 },
  Nitrogen_Level: { label: "Nitrogen Level", min: 0, max: 500, step: 1, unit: "ppm" },
  Phosphorus_Level: { label: "Phosphorus Level", min: 0, max: 500, step: 1, unit: "ppm" },
  Potassium_Level: { label: "Potassium Level", min: 0, max: 500, step: 1, unit: "ppm" },
  Chlorophyll_Content: { label: "Chlorophyll Content", min: 0, max: 100, step: 0.1, unit: "SPAD" },
  Electrochemical_Signal: { label: "Electrochemical Signal", min: 0, max: 10, step: 0.01 },
};

function parsePercent(text) {
  // input from backend is like "92.15%"
  const n = Number(String(text || "").replace("%", ""));
  return Number.isFinite(n) ? n : null;
}

function getStatusColor(status) {
  if (status === "Healthy") return "#1b7f2a";
  if (status === "Moderate Stress") return "#c77700";
  if (status === "High Stress") return "#b00020";
  return "#333";
}

function validateField(name, rawValue) {
  const rule = FIELD_RULES[name];
  if (!rule) return "";

  if (rawValue === "" || rawValue === null || rawValue === undefined) {
    return "Required";
  }

  const value = Number(rawValue);
  if (!Number.isFinite(value)) return "Must be a valid number";

  if (rule.min !== undefined && value < rule.min) return `Must be ≥ ${rule.min}`;
  if (rule.max !== undefined && value > rule.max) return `Must be ≤ ${rule.max}`;

  return "";
}

export default function Predict() {
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
    Electrochemical_Signal: "",
  });

  const [fieldErrors, setFieldErrors] = useState({});
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const confidenceValue = useMemo(() => parsePercent(result?.confidence), [result]);

  const validateAll = () => {
    const next = {};
    for (const key of Object.keys(formData)) {
      next[key] = validateField(key, formData[key]);
    }
    setFieldErrors(next);
    return Object.values(next).every((msg) => !msg);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    // Inline validation while typing
    setFieldErrors((prev) => ({ ...prev, [name]: validateField(name, value) }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    if (!validateAll()) {
      setError("Please fix the highlighted fields and try again.");
      return;
    }

    setLoading(true);
    try {
      const response = await predictPlantHealth(formData);
      setResult(response);
    } catch (err) {
      setError(err?.response?.data?.error || "❌ Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 16, maxWidth: 900, margin: "0 auto" }}>
      <h2 style={{ marginBottom: 6 }}>Plant Health Prediction</h2>
      <div style={{ color: "#555", marginBottom: 16 }}>
        Enter sensor values to predict plant health. Fields are validated before submission.
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: 16 }}>
        {/* FORM */}
        <div style={{ border: "1px solid #ddd", borderRadius: 10, padding: 16 }}>
          <h3 style={{ marginTop: 0 }}>Input Parameters</h3>

          <form onSubmit={handleSubmit}>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
                gap: 12,
              }}
            >
              {Object.keys(formData).map((key) => {
                const rule = FIELD_RULES[key] || { label: key };
                const errMsg = fieldErrors[key];
                const label = rule.unit ? `${rule.label} (${rule.unit})` : rule.label;

                return (
                  <div key={key}>
                    <label htmlFor={key} style={{ display: "block", fontWeight: 600, marginBottom: 4 }}>
                      {label}
                    </label>
                    <input
                      id={key}
                      type="number"
                      name={key}
                      value={formData[key]}
                      onChange={handleChange}
                      onBlur={() => setFieldErrors((prev) => ({ ...prev, [key]: validateField(key, formData[key]) }))}
                      required
                      min={rule.min}
                      max={rule.max}
                      step={rule.step}
                      style={{
                        width: "100%",
                        padding: 8,
                        borderRadius: 8,
                        border: errMsg ? "1px solid crimson" : "1px solid #bbb",
                      }}
                    />
                    {errMsg ? (
                      <div style={{ color: "crimson", fontSize: 12, marginTop: 4 }}>{errMsg}</div>
                    ) : (
                      <div style={{ color: "#777", fontSize: 12, marginTop: 4 }}>
                        Range: {rule.min} to {rule.max}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            <div style={{ display: "flex", gap: 10, marginTop: 14, alignItems: "center" }}>
              <button type="submit" disabled={loading} style={{ padding: "8px 14px" }}>
                {loading ? "Predicting..." : "Predict"}
              </button>
              {loading && <span style={{ color: "#555" }}>Running model inference…</span>}
            </div>
          </form>

          {error && (
            <div style={{ marginTop: 12, padding: 10, background: "#ffecec", border: "1px solid #ffbdbd", borderRadius: 8 }}>
              <strong style={{ color: "#b00020" }}>Error:</strong> {error}
            </div>
          )}
        </div>

        {/* RESULT */}
        <div style={{ border: "1px solid #ddd", borderRadius: 10, padding: 16 }}>
          <h3 style={{ marginTop: 0 }}>Result</h3>

          {!result ? (
            <div style={{ color: "#666" }}>Submit the form to see a prediction result.</div>
          ) : (
            <div>
              <div
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: 14,
                  alignItems: "center",
                  marginBottom: 10,
                }}
              >
                <div
                  style={{
                    padding: "6px 12px",
                    borderRadius: 999,
                    background: getStatusColor(result.prediction),
                    color: "white",
                    fontWeight: 700,
                  }}
                >
                  {result.prediction}
                </div>

                <div style={{ fontSize: 14 }}>
                  <strong>Confidence:</strong> {result.confidence}
                </div>
              </div>

              {/* Confidence Bar */}
              {confidenceValue !== null && (
                <div style={{ marginBottom: 14 }}>
                  <div
                    style={{
                      background: "#eee",
                      borderRadius: 999,
                      overflow: "hidden",
                      height: 20,
                    }}
                  >
                    <div
                      style={{
                        width: `${Math.max(0, Math.min(100, confidenceValue))}%`,
                        background: getStatusColor(result.prediction),
                        height: "100%",
                      }}
                    />
                  </div>
                  <div style={{ fontSize: 12, color: "#777", marginTop: 6 }}>{confidenceValue}%</div>
                </div>
              )}

              {/* Model Version */}
              <div style={{ marginBottom: 14 }}>
                <h4 style={{ margin: "10px 0 6px" }}>Model Version</h4>
                <div style={{ color: "#444" }}>
                  <div>
                    <strong>Version:</strong> {result.model_version || "unknown"}
                  </div>
                  {result.model_trained_at_utc && (
                    <div>
                      <strong>Trained at (UTC):</strong> {result.model_trained_at_utc}
                    </div>
                  )}
                </div>
              </div>

              {/* Explanation / Feature importance */}
              <div style={{ marginBottom: 14 }}>
                <h4 style={{ margin: "10px 0 6px" }}>Explanation (Top factors)</h4>
                {Array.isArray(result.explanation) && result.explanation.length > 0 ? (
                  <ul style={{ marginTop: 0 }}>
                    {result.explanation.map((item, idx) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>
                ) : (
                  <div style={{ color: "#666" }}>No explanation returned.</div>
                )}
              </div>

              {/* Plant message / recommendations */}
              <div style={{ marginBottom: 14 }}>
                <h4 style={{ margin: "10px 0 6px" }}>Recommendations</h4>
                {result.plant_message?.plant_message ? (
                  <div
                    style={{
                      padding: 12,
                      borderRadius: 8,
                      background: "#f6f8ff",
                      border: "1px solid #dbe2ff",
                    }}
                  >
                    <div style={{ marginBottom: 6 }}>
                      <strong>Mood:</strong> {result.plant_message?.plant_mood || "-"}
                    </div>
                    <div>{result.plant_message.plant_message}</div>
                  </div>
                ) : (
                  <div style={{ color: "#666" }}>No recommendations returned.</div>
                )}
              </div>

              {/* Report */}
              {result.report && (
                <button
                  style={{ padding: "8px 14px" }}
                  onClick={() => downloadFile(result.report, "plant-health-report.pdf")}
                >
                  Download Health Report (PDF)
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
