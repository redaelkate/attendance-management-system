import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { FaUserShield, FaKey, FaSignInAlt } from "react-icons/fa";

const AdminLogin = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [status, setStatus] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [statusType, setStatusType] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    if (!username || !password) {
      setStatus("Please enter both username and password.");
      setStatusType("error");
      return;
    }

    try {
      setIsLoading(true);
      setStatus("Authenticating...");
      setStatusType("info");
      
      const res = await axios.post("http://localhost:5000/login", {
        username,
        password
      });

      if (res.data === "success") {
        setStatus("Login successful! Redirecting to dashboard...");
        setStatusType("success");
        setTimeout(() => {
          navigate("/powerbi"); // Redirect to today's attendance
        }, 1000);
      } else {
        setStatus("Login failed. Incorrect credentials.");
        setStatusType("error");
      }
    } catch (err) {
      setStatus("Login error. Please try again.");
      setStatusType("error");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="card max-w-md mx-auto">
      <div className="text-center mb-6">
        <FaUserShield className="text-primary text-5xl mx-auto mb-4" />
        <h2 className="text-2xl font-semibold">Admin Login</h2>
        <p className="text-gray-500">Sign in to access the admin dashboard</p>
      </div>
      
      <div className="form-group">
        <label htmlFor="username" className="form-label">
          Username
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
            <FaUserShield className="text-gray-400" />
          </div>
          <input
            type="text"
            id="username"
            className="form-control pl-10"
            placeholder="Enter your username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
      </div>
      
      <div className="form-group">
        <label htmlFor="password" className="form-label">
          Password
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
            <FaKey className="text-gray-400" />
          </div>
          <input
            type="password"
            id="password"
            className="form-control pl-10"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
      </div>
      
      <button 
        className="btn btn-primary w-full" 
        onClick={handleLogin}
        disabled={isLoading}
      >
        {isLoading ? (
          "Logging in..."
        ) : (
          <>
            <FaSignInAlt className="mr-2" /> Login
          </>
        )}
      </button>
      
      {status && (
        <div className={`alert alert-${statusType} mt-4`}>
          {status}
        </div>
      )}
    </div>
  );
};

export default AdminLogin;
