import React, { useState, useEffect } from "react";
import { getAllPredictions, deletePrediction, updatePrediction, createPrediction } from "../services/api";
import { getToken } from "../utils/authStorage";
import { useNavigate } from "react-router-dom";
import "./Admin.css";

function Admin() {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({});
  const [showAddForm, setShowAddForm] = useState(false);
  const [addForm, setAddForm] = useState({
    user_id: "",
    prediction: "",
    confidence: "",
    input: {
      nitrogen: "",
      phosphorus: "",
      potassium: "",
      temperature: "",
      humidity: "",
      ph: "",
      rainfall: "",
      soil_moisture: "",
      sunlight_hours: "",
      plant_age_days: "",
      leaf_color_score: "",
      pest_presence: ""
    }
  });
  
  const navigate = useNavigate();

  useEffect(() => {
    const token = getToken();
    if (!token) {
      navigate("/login");
      return;
    }
    
    fetchPredictions();
  }, [navigate]);

  const fetchPredictions = async () => {
    try {
      setLoading(true);
      setError("");
      const data = await getAllPredictions(100, 0);
      setPredictions(data.predictions || []);
    } catch (err) {
      if (err?.response?.status === 403) {
        setError("Admin access required. You don't have permission to view this page.");
      } else {
        setError(err?.response?.data?.error || "Failed to load predictions");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this prediction?")) {
      return;
    }

    try {
      setError("");
      setSuccess("");
      await deletePrediction(id);
      setSuccess("Prediction deleted successfully");
      fetchPredictions();
    } catch (err) {
      setError(err?.response?.data?.error || "Failed to delete prediction");
    }
  };

  const handleEdit = (prediction) => {
    setEditingId(prediction._id);
    setEditForm({
      prediction: prediction.prediction || "",
      confidence: prediction.confidence || "",
      confidence_percent: prediction.confidence_percent || "",
      confidence_text: prediction.confidence_text || "",
      plant_message: prediction.plant_message || ""
    });
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setEditForm({});
  };

  const handleSaveEdit = async (id) => {
    try {
      setError("");
      setSuccess("");
      await updatePrediction(id, editForm);
      setSuccess("Prediction updated successfully");
      setEditingId(null);
      setEditForm({});
      fetchPredictions();
    } catch (err) {
      setError(err?.response?.data?.error || "Failed to update prediction");
    }
  };

  const handleAddFormChange = (field, value) => {
    if (field.startsWith("input.")) {
      const inputField = field.split(".")[1];
      setAddForm(prev => ({
        ...prev,
        input: {
          ...prev.input,
          [inputField]: value
        }
      }));
    } else {
      setAddForm(prev => ({
        ...prev,
        [field]: value
      }));
    }
  };

  const handleAddPrediction = async (e) => {
    e.preventDefault();
    
    try {
      setError("");
      setSuccess("");
      
      // Convert input values to numbers
      const processedInput = {};
      Object.keys(addForm.input).forEach(key => {
        const val = addForm.input[key];
        processedInput[key] = val === "" ? 0 : parseFloat(val);
      });
      
      const payload = {
        ...addForm,
        confidence: addForm.confidence === "" ? 0 : parseFloat(addForm.confidence),
        input: processedInput
      };
      
      await createPrediction(payload);
      setSuccess("Prediction created successfully");
      setShowAddForm(false);
      setAddForm({
        user_id: "",
        prediction: "",
        confidence: "",
        input: {
          nitrogen: "",
          phosphorus: "",
          potassium: "",
          temperature: "",
          humidity: "",
          ph: "",
          rainfall: "",
          soil_moisture: "",
          sunlight_hours: "",
          plant_age_days: "",
          leaf_color_score: "",
          pest_presence: ""
        }
      });
      fetchPredictions();
    } catch (err) {
      setError(err?.response?.data?.error || "Failed to create prediction");
    }
  };

  if (loading) {
    return (
      <div className="admin-container">
        <h2>Admin Dashboard</h2>
        <p>Loading predictions...</p>
      </div>
    );
  }

  return (
    <div className="admin-container">
      <h2>Admin Dashboard - Manage Predictions</h2>
      
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <div className="admin-actions">
        <button 
          className="btn-add" 
          onClick={() => setShowAddForm(!showAddForm)}
        >
          {showAddForm ? "Cancel Add" : "➕ Add New Prediction"}
        </button>
        <button className="btn-refresh" onClick={fetchPredictions}>
          🔄 Refresh
        </button>
      </div>

      {showAddForm && (
        <div className="add-form-container">
          <h3>Add New Prediction</h3>
          <form onSubmit={handleAddPrediction} className="add-form">
            <div className="form-row">
              <div className="form-group">
                <label>User ID *</label>
                <input
                  type="text"
                  value={addForm.user_id}
                  onChange={(e) => handleAddFormChange("user_id", e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label>Prediction *</label>
                <input
                  type="text"
                  value={addForm.prediction}
                  onChange={(e) => handleAddFormChange("prediction", e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label>Confidence (0-1)</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  max="1"
                  value={addForm.confidence}
                  onChange={(e) => handleAddFormChange("confidence", e.target.value)}
                />
              </div>
            </div>

            <h4>Input Parameters</h4>
            <div className="form-row">
              <div className="form-group">
                <label>Nitrogen</label>
                <input
                  type="number"
                  value={addForm.input.nitrogen}
                  onChange={(e) => handleAddFormChange("input.nitrogen", e.target.value)}
                />
              </div>
              <div className="form-group">
                <label>Phosphorus</label>
                <input
                  type="number"
                  value={addForm.input.phosphorus}
                  onChange={(e) => handleAddFormChange("input.phosphorus", e.target.value)}
                />
              </div>
              <div className="form-group">
                <label>Potassium</label>
                <input
                  type="number"
                  value={addForm.input.potassium}
                  onChange={(e) => handleAddFormChange("input.potassium", e.target.value)}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Temperature</label>
                <input
                  type="number"
                  value={addForm.input.temperature}
                  onChange={(e) => handleAddFormChange("input.temperature", e.target.value)}
                />
              </div>
              <div className="form-group">
                <label>Humidity</label>
                <input
                  type="number"
                  value={addForm.input.humidity}
                  onChange={(e) => handleAddFormChange("input.humidity", e.target.value)}
                />
              </div>
              <div className="form-group">
                <label>pH</label>
                <input
                  type="number"
                  step="0.1"
                  value={addForm.input.ph}
                  onChange={(e) => handleAddFormChange("input.ph", e.target.value)}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Rainfall</label>
                <input
                  type="number"
                  value={addForm.input.rainfall}
                  onChange={(e) => handleAddFormChange("input.rainfall", e.target.value)}
                />
              </div>
              <div className="form-group">
                <label>Soil Moisture</label>
                <input
                  type="number"
                  value={addForm.input.soil_moisture}
                  onChange={(e) => handleAddFormChange("input.soil_moisture", e.target.value)}
                />
              </div>
              <div className="form-group">
                <label>Sunlight Hours</label>
                <input
                  type="number"
                  value={addForm.input.sunlight_hours}
                  onChange={(e) => handleAddFormChange("input.sunlight_hours", e.target.value)}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Plant Age (Days)</label>
                <input
                  type="number"
                  value={addForm.input.plant_age_days}
                  onChange={(e) => handleAddFormChange("input.plant_age_days", e.target.value)}
                />
              </div>
              <div className="form-group">
                <label>Leaf Color Score</label>
                <input
                  type="number"
                  value={addForm.input.leaf_color_score}
                  onChange={(e) => handleAddFormChange("input.leaf_color_score", e.target.value)}
                />
              </div>
              <div className="form-group">
                <label>Pest Presence</label>
                <input
                  type="number"
                  value={addForm.input.pest_presence}
                  onChange={(e) => handleAddFormChange("input.pest_presence", e.target.value)}
                />
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="btn-submit">Create Prediction</button>
              <button type="button" className="btn-cancel" onClick={() => setShowAddForm(false)}>Cancel</button>
            </div>
          </form>
        </div>
      )}

      <div className="predictions-table-container">
        <p>Total Predictions: {predictions.length}</p>
        
        {predictions.length === 0 ? (
          <p>No predictions found.</p>
        ) : (
          <table className="predictions-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>User ID</th>
                <th>Prediction</th>
                <th>Confidence</th>
                <th>Timestamp</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {predictions.map((pred) => (
                <tr key={pred._id}>
                  <td>{pred._id.substring(0, 8)}...</td>
                  <td>{pred.user_id?.substring(0, 8)}...</td>
                  <td>
                    {editingId === pred._id ? (
                      <input
                        type="text"
                        value={editForm.prediction}
                        onChange={(e) => setEditForm({...editForm, prediction: e.target.value})}
                      />
                    ) : (
                      pred.prediction
                    )}
                  </td>
                  <td>
                    {editingId === pred._id ? (
                      <input
                        type="number"
                        step="0.01"
                        value={editForm.confidence}
                        onChange={(e) => setEditForm({...editForm, confidence: e.target.value})}
                        style={{ width: "80px" }}
                      />
                    ) : (
                      pred.confidence_percent || `${(pred.confidence * 100).toFixed(1)}%`
                    )}
                  </td>
                  <td>{new Date(pred.timestamp).toLocaleString()}</td>
                  <td className="actions">
                    {editingId === pred._id ? (
                      <>
                        <button className="btn-save" onClick={() => handleSaveEdit(pred._id)}>
                          ✓ Save
                        </button>
                        <button className="btn-cancel-edit" onClick={handleCancelEdit}>
                          ✕ Cancel
                        </button>
                      </>
                    ) : (
                      <>
                        <button className="btn-edit" onClick={() => handleEdit(pred)}>
                          ✏️ Edit
                        </button>
                        <button className="btn-delete" onClick={() => handleDelete(pred._id)}>
                          🗑️ Delete
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default Admin;
