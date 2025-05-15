import React, { useState, useRef } from "react";
import Webcam from "react-webcam";
import { FaCamera, FaArrowLeft } from "react-icons/fa";
import { Link } from "react-router-dom";

const Recognition = () => {
  const webcamRef = useRef<Webcam>(null);
  const [cameraLoading, setCameraLoading] = useState(true);
  const [status, setStatus] = useState("");
  const [statusType, setStatusType] = useState("");

  const handleCameraError = () => {
    setCameraLoading(false);
    setStatus("Webcam is not available. Please check your camera permissions.");
    setStatusType("error");
  };

  const capture = () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        setStatus("Image captured successfully! Processing...");
        setStatusType("success");
        // ...process the captured image...
      } else {
        setStatus("Failed to capture image. Please ensure your camera is working properly.");
        setStatusType("error");
      }
    } else {
      setStatus("Webcam is not available. Please check your camera permissions.");
      setStatusType("error");
    }
  };

  return (
    <>
      <Link to="/" className="back-link">
        <FaArrowLeft /> Back to Home
      </Link>

      <div className="card">
        <div className="card-header">
          <h2>Recognize Employee</h2>
        </div>

        <div className="webcam-container">
          <label className="form-label">Capture Photo</label>
          <div className="webcam-wrapper">
            {cameraLoading && (
              <div className="loading-spinner flex justify-center items-center h-60">
                <span className="inline-block animate-spin rounded-full h-10 w-10 border-t-4 border-b-4 border-gray-500"></span>
              </div>
            )}
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              width="100%"
              height="auto"
              videoConstraints={{
                facingMode: "user",
                width: 320,
                height: 240,
              }}
              onUserMedia={() => setCameraLoading(false)}
              onUserMediaError={handleCameraError}
            />
          </div>

          <div className="webcam-controls">
            <button 
              type="button" 
              className="btn btn-primary"
              onClick={capture}
            >
              <FaCamera className="mr-2" /> Capture Image
            </button>
          </div>
        </div>

        {status && (
          <div className={`alert alert-${statusType} my-4`}>
            {status}
          </div>
        )}
      </div>
    </>
  );
};

export default Recognition;
