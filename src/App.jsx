import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import LessonPage from "./pages/LessonPage";
import Login from "./pages/Login";
import Leaderboard from "./pages/Leaderboard";

export default function App(){
  const token = localStorage.getItem("token");
  return (
    <Router>
      <div className="p-6">
        <nav className="flex gap-4 mb-6">
          <Link to="/">Dashboard</Link>
          <Link to="/leaderboard">Leaderboard</Link>
          {!token && <Link to="/login">Login / Register</Link>}
          {token && <button onClick={()=>{
            localStorage.removeItem("token"); localStorage.removeItem("user_id"); window.location.reload();
          }}>Logout</button>}
        </nav>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/lesson/:id" element={<LessonPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
        </Routes>
      </div>
    </Router>
  )
}
