import React, { useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import { Chart, BarElement, CategoryScale, LinearScale } from "chart.js";
import "../../style/Spiral.css";
import { Link,useNavigate } from "react-router-dom";
import handleLogout from "../helpers/handle_logout";

Chart.register(BarElement, CategoryScale, LinearScale);

export default function Spiral() {
  const [imageFile, setImageFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const navigate = useNavigate();

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImageFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null); // Clear previous result
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!imageFile) {
      setError("Please upload an image.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", imageFile); // Update key to "file" as per backend expectation

      const response = await axios.post("http://localhost:5000/api/predict", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const { class_name, confidence_score } = response.data;

      setResult({ class_name, confidence_score });
    } catch (err) {
      console.error("Prediction failed:", err);
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">

      <nav className="navbar">
        <div className="nav-logo">Parkinsons Prediction</div>
        <div className="nav-links">
          <Link to="/home">Home</Link>
          <Link to="/spiral">Spiral</Link>
          <Link to="/gait">Gait</Link>
          <Link to="/bradykinesia">Bradykinesia</Link>
          <Link to="/tremors">Tremors</Link>
          <button onClick={()=>handleLogout(navigate)} >Logout</button>
        </div>
      </nav>

      <div className="upload-card">
        <h2>Upload Hand Image</h2>
        <p>Select an image for prediction.</p>

        <form onSubmit={handleSubmit} className="form-container">
          <div className="form-group">
            <label>Upload Image</label>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              required
            />
          </div>

          {error && <p className="error">{error}</p>}

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? "Processing..." : "Submit for Prediction"}
          </button>
        </form>

        <p className="note">Your image will be securely analyzed.</p>
        <hr />
        <h4>{result!==null? `Class: ${result.class_name}`:null}</h4>
        <h2>{result!==null && result.class_name==="patient"?"Sign of Parkinsons detected":"No signs of parkinsons detected"}</h2>

        {result && (
          <div className="result-section">
            <div className="result-container">
              {/* Result Section */}
              <div className="prediction">
                <h3>Spiral drawing</h3>
                {previewUrl && (
                  <img src={previewUrl} alt="Uploaded preview" className="preview-image" />
                )}
                
              </div>

              {/* Confidence Score Bar */}

              <div className="chart-wrapper">
                <h3>Confidence chart</h3>
                <Bar
                  data={{
                    labels: [result.class_name],
                    datasets: [
                      {
                        label: "Confidence Score",
                        data: [result.confidence_score * 100], // Convert to percentage
                        backgroundColor: "#4CAF50",
                      },
                    ],
                  }}
                  options={{
                    indexAxis: 'y', // Set to 'y' for vertical bars
                    scales: {
                      x: {
                        min: 0,
                        max: 100,
                        ticks: { callback: (val) => `${val}%` }, // Display percentage ticks
                      },
                      y: {
                        beginAtZero: true, // Ensure the y-axis starts at 0
                      },
                    },
                  }}
                />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
