import React from "react";
import { Navigate } from "react-router-dom";
import { getToken, isTokenExpired, clearToken } from "../utils/authStorage";

export default function ProtectedRoute({ children }) {
  const token = getToken();

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (isTokenExpired(token)) {
    clearToken();
    return <Navigate to="/login" replace />;
  }

  return children;
}
