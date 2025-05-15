import React, { useRef, useState } from "react";
import Webcam from "react-webcam";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import { FaCamera, FaCheck, FaSignInAlt, FaSignOutAlt, FaArrowLeft, FaUser } from "react-icons/fa";

const AttendanceConfirmation = () => {
  const webcamRef = useRef<Webcam>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [status, setStatus] = useState("");
  const [statusType, setStatusType] = useState("");
  const [recognizedName, setRecognizedName] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showFaceDetectionBox, setShowFaceDetectionBox] = useState(false);
  const navigate = useNavigate();

  const captureAndRecognize = async () => {
    const canvas = canvasRef.current;
    const video = webcamRef.current ? webcamRef.current.video : null;

    if (!video) {
      setStatus("Webcam not ready. Please ensure your camera is connected and permissions are granted.");
      setStatusType("error");
      return;
    }

    if (!canvas) {
      setStatus("Canvas not available");
      setStatusType("error");
      return;
    }

    setIsProcessing(true);
    setStatus("Processing your image. Please wait...");
    setStatusType("info");
    
    try {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext("2d")?.drawImage(video, 0, 0);
      const image = canvas.toDataURL("image/jpeg");

      const res = await axios.post("http://localhost:5000/recognize_face", {
        image,
        mode: "recognize"
      });

      if (res.data.name && res.data.name !== "Unknown") {
        setRecognizedName(res.data.name);
        setStatus(`Welcome, ${res.data.name}! Please mark your attendance.`);
        setStatusType("success");
      } else {
        setStatus("No registered face detected. Please try again or register if you're a new employee.");
        setStatusType("error");
      }
    } catch (err) {
      setStatus("Error recognizing face. Please try again.");
      setStatusType("error");
    } finally {
      setIsProcessing(false);
    }
  };

  const markAttendance = async (mode: "entry" | "exit") => {
    if (!recognizedName) {
      setStatus("No recognized user. Please scan your face first.");
      setStatusType("error");
      return;
    }

    setIsProcessing(true);
    setStatus(`Marking ${mode === "entry" ? "entry" : "exit"}...`);
    setStatusType("info");

    try {
      const res = await axios.post("http://localhost:5000/mark_attendance", {
        name: recognizedName,
        mode
      });

      setStatus(res.data.message || `${mode === "entry" ? "Entry" : "Exit"} marked successfully!`);
      setStatusType("success");
      
      // Navigate to success page after a short delay
      setTimeout(() => {
        navigate("/success");
      }, 1500);
    } catch (err) {
      setStatus(`Error marking ${mode}. Please try again.`);
      setStatusType("error");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <>
      <Link to="/" className="back-link">
        <FaArrowLeft /> Back to Home
      </Link>
      
      <div className="card">
        <div className="card-header">
          <h2>Attendance Confirmation</h2>
        </div>
        
        <div className="webcam-container">
          <div className="webcam-wrapper">
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              width="100%"
              height="auto"
              videoConstraints={{
                facingMode: "user"
              }}
            />
            {showFaceDetectionBox && (
              <div className="face-detection-box"></div>
            )}
          </div>
          <canvas ref={canvasRef} style={{ display: "none" }} />
          
          <div className="webcam-controls">
            <button 
              className="btn btn-primary w-full"
              onClick={captureAndRecognize}
              disabled={isProcessing}
            >
              {isProcessing ? (
                <>
                  <span className="inline-block animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white mr-2"></span>
                  Processing...
                </>
                ) : (
                <>
                  <FaCamera className="mr-2" /> Recognize Face
                </>
              )}
            </button>
          </div>
        </div>
        
        {status && (
          <div className={`alert alert-${statusType} mb-4`}>
            {statusType === "success" && <FaCheck className="text-success" />}
            {status}
          </div>
        )}
        
        {recognizedName && (
          <div className="card bg-gray-50 mb-4">
            <div className="flex items-center">
              <div className="bg-primary text-white rounded-full p-3 mr-4">
                <FaUser className="text-2xl" />
              </div>
              <div>
                <h3 className="font-medium text-lg">{recognizedName}</h3>
                <p className="text-gray-500">Employee</p>
              </div>
            </div>
            
            <div className="btn-group mt-4">
              <button 
                className="btn btn-success" 
                onClick={() => markAttendance("entry")}
                disabled={isProcessing}
              >
                <FaSignInAlt className="mr-2" /> Mark Entry
              </button>
              <button 
                className="btn btn-danger" 
                onClick={() => markAttendance("exit")}
                disabled={isProcessing}
              >
                <FaSignOutAlt className="mr-2" /> Mark Exit
              </button>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default AttendanceConfirmation;