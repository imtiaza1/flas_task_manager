import { useEffect, useState } from "react";
import { Toaster } from "react-hot-toast";
import { Navigate, Route, Routes } from "react-router-dom";
import api from "./axios";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Register from "./pages/Register";

function App() {
  const [loading, setLoading] = useState(true);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // 🔑 Check login from backend
  useEffect(() => {
    api
      .get("/auth/check")
      .then((res) => {
        if (res.data.success) {
          setIsLoggedIn(true);
        } else {
          setIsLoggedIn(false);
        }
        setLoading(false);
      })
      .catch(() => {
        setIsLoggedIn(false);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-white">Checking session...</div>;

  return (
    <>
      <Toaster position="top-right" />
      <Routes>
        <Route
          path="/login"
          element={
            isLoggedIn ? (
              <Navigate to="/dashboard" />
            ) : (
              <Login setIsLoggedIn={setIsLoggedIn} />
            )
          }
        />
        <Route path="/register" element={<Register />} />
        <Route
          path="/dashboard"
          element={
            isLoggedIn ? (
              <Dashboard setIsLoggedIn={setIsLoggedIn} />
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </>
  );
}

export default App;
