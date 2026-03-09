import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { clearToken, getToken, isTokenExpired, getUserRole } from "../utils/authStorage";

export default function NavBar() {
  const navigate = useNavigate();
  const token = getToken();
  const isAuthed = token && !isTokenExpired(token);
  const userRole = getUserRole();

  const logout = () => {
    clearToken();
    navigate("/login", { replace: true });
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "10px 16px",
        borderBottom: "1px solid #ddd",
      }}
    >
      <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
        <strong>🌱 Plant Health</strong>
        {isAuthed && (
          <>
            <Link to="/predict">Predict</Link>
            <Link to="/history">History</Link>
            {userRole === "admin" && (
              <Link to="/admin" style={{ color: "#f44336", fontWeight: "bold" }}>
                Admin
              </Link>
            )}
          </>
        )}
      </div>

      <div>
        {isAuthed ? (
          <button onClick={logout}>Logout</button>
        ) : (
          <div style={{ display: "flex", gap: 10 }}>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </div>
        )}
      </div>
    </div>
  );
}
