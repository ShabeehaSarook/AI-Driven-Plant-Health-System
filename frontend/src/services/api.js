import axios from "axios";
import { clearToken, getToken, isTokenExpired } from "../utils/authStorage";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000";

const API = axios.create({
  baseURL: API_URL,
});

// Attach Authorization header automatically
API.interceptors.request.use((config) => {
  const token = getToken();
  if (token && !isTokenExpired(token)) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// On 401, clear token so UI forces re-login
API.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error?.response?.status === 401) {
      clearToken();
    }
    return Promise.reject(error);
  }
);

export async function register(payload) {
  const res = await API.post("/register", payload);
  return res.data;
}

export async function login(payload) {
  const res = await API.post("/login", payload);
  return res.data;
}

export async function predictPlantHealth(data) {
  const res = await API.post("/predict", data);
  return res.data;
}

export async function getHistory(limit = 50) {
  const res = await API.get(`/history?limit=${encodeURIComponent(limit)}`);
  return res.data;
}

export async function regenerateReport(predictionId) {
  const res = await API.post(`/predictions/${encodeURIComponent(predictionId)}/report/regenerate`);
  return res.data;
}

// Admin APIs
export async function getAllPredictions(limit = 100, skip = 0) {
  const res = await API.get(`/admin/predictions?limit=${limit}&skip=${skip}`);
  return res.data;
}

export async function deletePrediction(predictionId) {
  const res = await API.delete(`/admin/predictions/${encodeURIComponent(predictionId)}`);
  return res.data;
}

export async function updatePrediction(predictionId, data) {
  const res = await API.put(`/admin/predictions/${encodeURIComponent(predictionId)}`, data);
  return res.data;
}

export async function createPrediction(data) {
  const res = await API.post(`/admin/predictions`, data);
  return res.data;
}

export default API;
