// Simple auth token storage helpers.
// Token is a JWT issued by the Flask backend.

const TOKEN_KEY = "token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY) || "";
}

export function setToken(token) {
  if (!token) return;
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

// Decode JWT payload without verifying signature.
// Used only for client-side expiration checks.
export function decodeJwt(token) {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return null;
    const payload = parts[1]
      .replace(/-/g, "+")
      .replace(/_/g, "/");
    const json = decodeURIComponent(
      atob(payload)
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    );
    return JSON.parse(json);
  } catch {
    return null;
  }
}

export function isTokenExpired(token) {
  const payload = decodeJwt(token);
  if (!payload || !payload.exp) return false; // If unknown, treat as not expired.
  const expMs = payload.exp * 1000;
  return Date.now() >= expMs;
}

export function getUserRole() {
  const token = getToken();
  if (!token) return null;
  const payload = decodeJwt(token);
  return payload?.role || "user";
}
