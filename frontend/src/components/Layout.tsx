import React from "react";
import { Link } from "react-router-dom";
import { FaUserCheck } from "react-icons/fa";

const Layout = ({ children }) => {
  return (
    <div className="app-container">
      <header className="header">
        <div className="container">
          <div className="header-content">
            <Link to="/" className="logo">
              <FaUserCheck className="logo-icon" />
              <h1>Check-in System</h1>
            </Link>
          </div>
        </div>
      </header>
      
      <main className="main-content">
        <div className="container">
          {children}
        </div>
      </main>
      
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            &copy; {new Date().getFullYear()} Face Recognition-based Attendance Management System
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;