import React from "react";
import { Link } from "react-router-dom";
import { FaCheckCircle, FaHome } from "react-icons/fa";

const SuccessPage = () => (
  <div className="card text-center">
    <div className="mb-6">
      <FaCheckCircle className="text-success text-6xl mx-auto mb-4" />
      <h2 className="text-2xl font-semibold">Attendance Marked Successfully!</h2>
      <p className="text-gray-500 mt-2">
        Your attendance has been recorded in the system.
      </p>
    </div>
    
    <Link to="/" className="btn btn-primary inline-flex items-center">
      <FaHome className="mr-2" /> Return to Home
    </Link>
  </div>
);

export default SuccessPage;
