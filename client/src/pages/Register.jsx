import { useState } from "react";
import toast from "react-hot-toast";
import { FaLock, FaUser } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import axios from "../axios";

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("/auth/register", {
        username,
        password,
      });

      if (res.data.success) {
        toast.success("User registered ✅");
        navigate("/login");
      }
    } catch (err) {
      console.log(err);
      toast.error(err.response.data.message || "Something went wrong");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900 text-white">
      <div className="w-full max-w-md p-8 space-y-6 bg-gray-800 rounded-2xl shadow-lg">
        <h2 className="text-3xl font-bold text-center">Create Account</h2>
        <form onSubmit={handleRegister} className="space-y-4">
          <div className="flex items-center border border-gray-600 rounded-lg px-3 py-2 bg-gray-700">
            <FaUser className="text-gray-400 mr-2" />
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-transparent outline-none text-white placeholder-gray-400"
              required
            />
          </div>

          <div className="flex items-center border border-gray-600 rounded-lg px-3 py-2 bg-gray-700">
            <FaLock className="text-gray-400 mr-2" />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-transparent outline-none text-white placeholder-gray-400"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full py-2 rounded-lg bg-blue-600 hover:bg-blue-700 transition font-semibold"
          >
            Register
          </button>
        </form>

        <p className="text-center text-gray-400">
          Already have an account?{" "}
          <span
            onClick={() => navigate("/login")}
            className="text-blue-400 cursor-pointer hover:underline"
          >
            Login
          </span>
        </p>
      </div>
    </div>
  );
}
