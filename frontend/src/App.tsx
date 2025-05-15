import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home.tsx";
import Register from "./pages/Register";
import AttendanceConfirmation from "./pages/AttendanceConfirmation.tsx";
import AttendanceToday from "./pages/AttendanceToday.tsx";
//import AttendanceAll from "./pages/AttendanceAll";
import AdminLogin from "./pages/AdminLogin.tsx";
import SuccessPage from "./pages/SuccessPage.tsx";
import ImageCaptured from "./pages/ImageCaptured.tsx";
import Layout from "./components/Layout";
import "./global.css";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout><Home /></Layout>} />
        <Route path="/register" element={<Layout><Register /></Layout>} />
        <Route path="/confirm" element={<Layout><AttendanceConfirmation /></Layout>} />
        <Route path="/today" element={<Layout><AttendanceToday /></Layout>} />
        {/*<Route path="/all" element={<Layout><AttendanceAll /></Layout>} */}
        <Route path="/login" element={<Layout><AdminLogin /></Layout>} />
        <Route path="/success" element={<Layout><SuccessPage /></Layout>} />
        <Route path="/captured" element={<Layout><ImageCaptured /></Layout>} />
      </Routes>
    </Router>
  );
}
