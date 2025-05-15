import React, { useState, useRef } from "react";
import Webcam from "react-webcam";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import { FaCamera, FaUser, FaIdCard, FaArrowLeft, FaSave } from "react-icons/fa";

const Register = () => {
  const webcamRef = useRef<Webcam>(null);
  const [name, setName] = useState("");
  const [regId, setRegId] = useState("");
  const [imageData, setImageData] = useState<string | null>(null);
  const [status, setStatus] = useState("");
  const [statusType, setStatusType] = useState("");
  const [preview, setPreview] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const navigate = useNavigate();

  const capture = () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        setImageData(imageSrc);
        setPreview(imageSrc);
        setStatus("Image captured successfully! You can retake if needed.");
        setStatusType("success");
      } else {
        setStatus("Failed to capture image. Please ensure your camera is working properly.");
        setStatusType("error");
      }
    } else {
      setStatus("Webcam is not available. Please check your camera permissions.");
      setStatusType("error");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) {
      setStatus("Please enter the employee name.");
      setStatusType("error");
      return;
    }
    
    if (!regId.trim()) {
      setStatus("Please enter the registration ID.");
      setStatusType("error");
      return;
    }
    
    if (!imageData) {
      setStatus("Please capture an image first.");
      setStatusType("error");
      return;
    }
    
    setIsProcessing(true);
    setStatus("Registering employee. Please wait...");
    setStatusType("info");
    
    try {
      const formData = new FormData();
      formData.append("name1", name.trim());
      formData.append("name2", regId.trim());
      formData.append("image_data", imageData);

      const res = await axios.post("http://localhost:5000/name", formData);
      
      setStatus(res.data.message || "Registration successful!");
      setStatusType("success");
      
      // Clear form
      setTimeout(() => {
        navigate("/captured");
      }, 1500);
    } catch (err) {
      setStatus(err.response?.data?.error || "Error during registration. Please try again.");
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
          <h2>Register New Employee</h2>
        </div>
        
        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <div className="form-group">
                <label htmlFor="name" className="form-label">Employee Name</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <FaUser className="text-gray-400" />
                  </div>
                  <input
                    type="text"
                    id="name"
                    className="form-control pl-10"
                    placeholder="Enter full name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                  />
                </div>
              </div>
              
              <div className="form-group">
                <label htmlFor="regId" className="form-label">Registration ID</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <FaIdCard className="text-gray-400" />
                  </div>
                  <input
                    type="text"
                    id="regId"
                    className="form-control pl-10"
                    placeholder="Enter employee ID"
                    value={regId}
                    onChange={(e) => setRegId(e.target.value)}
                    required
                  />
                </div>
              </div>
              
              {preview && (
                <div className="preview-container">
                  <div className="preview-image">
                    <img 
                      src={preview} 
                      alt="Preview" 
                      className="w-full rounded"
                    />
                  </div>
                  <p className="text-center text-sm text-gray-500">Preview Image</p>
                </div>
              )}
            </div>
            
            <div className="webcam-container">
              <label className="form-label">Capture Photo</label>
              <div className="webcam-wrapper">
                <Webcam
                  audio={false}
                  ref={webcamRef}
                  screenshotFormat="image/jpeg"
                  width="100%"
                  height="auto"
                  videoConstraints={{
                    facingMode: "user",
                    width: 320,
                    height: 240
                  }}
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
          </div>
          
          {status && (
            <div className={`alert alert-${statusType} my-4`}>
              {status}
            </div>
          )}
          
          <div className="form-group mt-4">
            <button 
              type="submit" 
              className="btn btn-success w-full md:w-auto"
              disabled={isProcessing || !imageData}
            >
              {isProcessing ? (
                <>
                  <span className="inline-block animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white mr-2"></span>
                  Registering...
                </>
              ) : (
                <>
                  <FaSave className="mr-2" /> Register Employee
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </>
  );
};

export default Register;
