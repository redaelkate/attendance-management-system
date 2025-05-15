import React from "react";
import { Link } from "react-router-dom";
import { FaUserPlus, FaFingerprint, FaUserShield } from "react-icons/fa";

const Home = () => {
  return (
    <>
      <div className="card">
        <div className="card-header">
          <h2>Welcome to FRAMS</h2>
        </div>
        <p className="text-lg mb-6">Face Recognition-based Attendance Management System</p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card">
            <div className="text-center mb-4">
              <FaUserPlus className="text-5xl mx-auto text-primary mb-3" />
              <h3 className="font-medium text-xl">Register</h3>
              <p className="text-gray-500">Add new employees to the system</p>
            </div>
            <Link to="/register" className="btn btn-primary w-full">
              Register Employee
            </Link>
          </div>
          
          <div className="card">
            <div className="text-center mb-4">
              <FaFingerprint className="text-5xl mx-auto text-primary mb-3" />
              <h3 className="font-medium text-xl">Attendance</h3>
              <p className="text-gray-500">Mark your daily attendance</p>
            </div>
            <Link to="/confirm" className="btn btn-primary w-full">
              Punch Attendance
            </Link>
          </div>
          
          <div className="card">
            <div className="text-center mb-4">
              <FaUserShield className="text-5xl mx-auto text-primary mb-3" />
              <h3 className="font-medium text-xl">Admin</h3>
              <p className="text-gray-500">Access admin dashboard</p>
            </div>
            <Link to="/login" className="btn btn-primary w-full">
              Admin Login
            </Link>
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;