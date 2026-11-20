import { useState } from "react";
import { BrowserRouter, Navigate, NavLink, Route, Routes } from "react-router-dom";
import AddProblem from "./pages/AddProblem.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Login from "./pages/Login.jsx";
import Today from "./pages/Today.jsx";

export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem("token"));

  function handleLogin(newToken) {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  }

  function handleLogout() {
    localStorage.removeItem("token");
    setToken(null);
  }

  if (!token) return <Login onLogin={handleLogin} />;

  return (
    <BrowserRouter>
      <header className="nav">
        <strong>DSA Revision Tracker</strong>
        <NavLink to="/">Today</NavLink>
        <NavLink to="/add">Add problem</NavLink>
        <NavLink to="/dashboard">Dashboard</NavLink>
        <button className="secondary" onClick={handleLogout}>Log out</button>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Today />} />
          <Route path="/add" element={<AddProblem />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}