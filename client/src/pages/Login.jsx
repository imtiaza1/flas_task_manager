import { useState } from "react";
import { toast } from "react-hot-toast";
import { FaLock, FaUser } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import api from "../axios";

export default function Login({ setIsLoggedIn }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post("/auth/login", { username, password });

      if (res.data.success) {
        toast.success("✅ Login Successful!");
        setIsLoggedIn(true); // update auth state
        navigate("/dashboard");
      } else {
        toast.error(res.data.message);
      }
    } catch (err) {
      console.log(err);
      toast.error("❌ Invalid credentials");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900 text-white">
      <div className="bg-gray-800 p-8 rounded-2xl shadow-lg w-96">
        <h2 className="text-2xl font-bold text-center mb-6">Login</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex items-center bg-gray-700 rounded-lg px-3 py-2">
            <FaUser className="text-gray-400 mr-2" />
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="bg-transparent outline-none w-full text-white"
              required
            />
          </div>

          <div className="flex items-center bg-gray-700 rounded-lg px-3 py-2">
            <FaLock className="text-gray-400 mr-2" />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="bg-transparent outline-none w-full text-white"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 transition-colors py-2 rounded-lg font-semibold"
          >
            Login
          </button>
        </form>

        <p className="text-sm text-gray-400 text-center mt-4">
          Don’t have an account?{" "}
          <span
            onClick={() => navigate("/register")}
            className="text-blue-400 cursor-pointer hover:underline"
          >
            Register
          </span>
        </p>
      </div>
    </div>
  );
}
