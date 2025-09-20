import { useEffect, useState } from "react";
import { toast } from "react-hot-toast";
import { FaSignOutAlt, FaTrash } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import api from "../axios";

export default function Dashboard({ user, setIsLoggedIn }) {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const navigate = useNavigate();

  const fetchTasks = () => {
    api
      .get("/task/", { withCredentials: true })
      .then((res) => setTasks(res.data.data))
      .catch(() => toast.error("Failed to fetch tasks"));
  };
  useEffect(() => {
    fetchTasks();
  }, []);
  // Add task
  const handleAddTask = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    try {
      const res = await api.post("/task/add", { title });
      if (res.data.success) {
        setTitle("");
        fetchTasks();
        toast.success("Task added ✅");
      } else {
        toast.error(res.data.message);
      }
    } catch {
      toast.error("Failed to add task ❌");
    }
  };

  // Delete task
  const handleDelete = async (id) => {
    try {
      await api.delete(`/task/delete/${id}`);
      fetchTasks();
      toast.success("Task deleted 🗑️");
    } catch {
      toast.error("Failed to delete ❌");
    }
  };

  // Change status
  const handleStatusChange = async (id, status) => {
    try {
      await api.put(`/task/toggle/${id}`, { status });
      fetchTasks();
      toast.success("Status updated 🔄");
    } catch {
      toast.error("Failed to update ❌");
    }
  };

  // Logout
  const handleLogout = async () => {
    await api.post("/auth/logout");
    localStorage.clear();
    setIsLoggedIn(false);
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Dashboard</h2>
        <p>WellCome {user}</p>
        <button
          onClick={handleLogout}
          className="flex items-center bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg"
        >
          <FaSignOutAlt className="mr-2" /> Logout
        </button>
      </div>

      {/* Add Task */}
      <form onSubmit={handleAddTask} className="flex mb-6 space-x-2">
        <input
          type="text"
          placeholder="New Task"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="flex-1 px-3 py-2 rounded-lg bg-gray-800 outline-none"
        />
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg"
        >
          Add
        </button>
      </form>

      {/* Task List */}
      <ul className="space-y-3">
        {tasks.map((t) => (
          <li
            key={t.id}
            className="flex justify-between items-center bg-gray-800 p-3 rounded-lg"
          >
            <div>
              <span className="font-semibold">{t.title}</span>{" "}
              <span className="text-sm text-gray-400">({t.status})</span>
            </div>
            <div className="flex items-center space-x-3">
              <select
                value={t.status}
                onChange={(e) => handleStatusChange(t.id, e.target.value)}
                className="bg-gray-700 px-2 py-1 rounded-lg"
              >
                <option>Pending</option>
                <option>Working</option>
                <option>Done</option>
              </select>
              <FaTrash
                onClick={() => handleDelete(t.id)}
                className="text-red-500 cursor-pointer hover:text-red-700"
              />
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
