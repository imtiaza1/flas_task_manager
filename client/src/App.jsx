import { useEffect, useState } from "react";
import { Toaster } from "react-hot-toast";
import { Navigate, Route, Routes } from "react-router-dom";
import api from "./axios";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Register from "./pages/Register";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState("");

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const res = await api.get("/auth/check"); // backend pe JWT verify karega
        if (res.data.success) {
          setIsLoggedIn(true);
          setUser(res.data.user.username);
        } else {
          setIsLoggedIn(false);
        }
      } catch (err) {
        console.log(err);
        setIsLoggedIn(false);
      }
    };

    checkAuth();
  }, [isLoggedIn]);
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
              <Dashboard user={user} setIsLoggedIn={setIsLoggedIn} />
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
