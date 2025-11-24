// frontend/src/pages/SearchPage.tsx
// Search page: upload resume + input filters → call /match API

import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { getMatchedJobs } from "../api/apiClient";

function SearchPage() {
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [location, setLocation] = useState("");
  const [experience, setExperience] = useState("0");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  // Handle resume file selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  // Handle form submit → call backend /match
  const handleSubmit = async () => {
    if (!file) {
      alert("Please upload your resume.");
      return;
    }
    if (!title || !location) {
      alert("Please enter job title and location.");
      return;
    }

    setLoading(true);

    // Prepare form data
    const formData = new FormData();
    formData.append("file", file);
    formData.append("title", title);
    formData.append("location", location);
    formData.append("experience", experience);

    // Call backend API
    let results = [];
    try {
      results = await getMatchedJobs(formData);
    } catch (err) {
      console.error(err);
      alert("Failed to match jobs. Please check backend.");
    }

    setLoading(false);

    // Navigate to result page with results data
    navigate("/result", { state: { results } });
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Search Jobs</h1>

      {/* Upload Resume */}
      <div style={{ marginBottom: "20px" }}>
        <label>Upload Resume:</label>
        <br />
        <input type="file" onChange={handleFileChange} style={{ marginTop: "8px" }} />
      </div>

      {/* Job Title */}
      <div style={{ marginBottom: "20px" }}>
        <label>Job Title:</label>
        <br />
        <input
          style={{ width: "300px", padding: "8px" }}
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
      </div>

      {/* Location */}
      <div style={{ marginBottom: "20px" }}>
        <label>Location:</label>
        <br />
        <input
          style={{ width: "300px", padding: "8px" }}
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
      </div>

      {/* Experience */}
      <div style={{ marginBottom: "20px" }}>
        <label>Experience:</label>
        <br />
        <select
          style={{ width: "200px", padding: "8px" }}
          value={experience}
          onChange={(e) => setExperience(e.target.value)}
        >
          <option value="0">0 years</option>
          <option value="1-3">1 - 3 years</option>
          <option value="3-5">3 - 5 years</option>
          <option value="5+">5+ years</option>
        </select>
      </div>

      {/* Submit */}
      <button
        onClick={handleSubmit}
        style={{
          padding: "12px 24px",
          fontSize: "18px",
          cursor: "pointer"
        }}
        disabled={loading}
      >
        {loading ? "Matching..." : "Search"}
      </button>
    </div>
  );
}

export default SearchPage;
