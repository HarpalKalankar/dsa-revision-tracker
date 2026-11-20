const API_URL = import.meta.env.VITE_API_URL;

// Calls the FastAPI backend. Adds the login token, sends JSON (or a form
// for login), and turns error responses into readable messages.
export async function api(path, { method = "GET", body, form } = {}) {
  const headers = {};
  const token = localStorage.getItem("token");
  if (token) headers.Authorization = `Bearer ${token}`;

  let payload;
  if (form) {
    payload = new URLSearchParams(form);
  } else if (body) {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);
  }

  const response = await fetch(`${API_URL}${path}`, { method, headers, body: payload });

  // Token expired or invalid: log out and go back to the login screen
  if (response.status === 401 && token) {
    localStorage.removeItem("token");
    window.location.href = "/";
    return null;
  }
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    if (typeof error.detail === "string") throw new Error(error.detail);
    if (Array.isArray(error.detail)) throw new Error(error.detail[0].msg);
    throw new Error("Something went wrong. Please try again.");
  }
  return response.status === 204 ? null : response.json();
}
