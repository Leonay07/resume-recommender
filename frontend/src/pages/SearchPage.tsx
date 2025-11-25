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

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

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

    const formData = new FormData();
    formData.append("file", file);
    formData.append("title", title);
    formData.append("location", location);
    formData.append("experience", experience);

    let results = [];
    try {
      results = await getMatchedJobs(formData);
    } catch (err) {
      console.error(err);
      alert("Failed to match jobs. Please check backend.");
    }

    setLoading(false);
    navigate("/result", { state: { results } });
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "48px 24px",
        background:
          "radial-gradient(circle at top, #4f7ccf 0%, #1b2b5a 55%, #0a1024 100%)",
        boxSizing: "border-box"
      }}
    >
      <div
        style={{
          width: "min(900px, 100%)",
          background:
            "linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.04))",
          borderRadius: "28px",
          border: "1px solid rgba(255, 255, 255, 0.2)",
          padding: "48px",
          color: "#f8fafc",
          boxShadow: "0 30px 80px rgba(8, 13, 32, 0.45)",
          backdropFilter: "blur(12px)"
        }}
      >
        <p
          style={{
            textTransform: "uppercase",
            letterSpacing: "0.2em",
            fontSize: "13px",
            color: "rgba(226, 232, 240, 0.8)",
            margin: "0 0 12px"
          }}
        >
          Resume Match
        </p>
        <h1 style={{ margin: "0 0 24px" }}>Upload your resume & tailor the search</h1>
        <p style={{ margin: "0 0 32px", color: "rgba(226,232,240,0.75)", lineHeight: 1.6 }}>
          Provide a recent resume and a few preferences so our matching engine can prioritise the
          most relevant openings for you.
        </p>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: "24px"
          }}
        >
          <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
            <label style={{ fontWeight: 600 }}>Upload Resume</label>
            <label
              htmlFor="resume-upload"
              style={{
                border: "2px dashed rgba(255,255,255,0.3)",
                borderRadius: "18px",
                padding: "24px",
                textAlign: "center",
                cursor: "pointer",
                backgroundColor: "rgba(255,255,255,0.04)"
              }}
            >
              <p style={{ margin: 0, fontWeight: 600 }}>
                {file ? file.name : "Drag & drop or click to upload"}
              </p>
              <p style={{ margin: "8px 0 0", fontSize: "14px", color: "rgba(226,232,240,0.7)" }}>
                PDF
              </p>
            </label>
            <input
              id="resume-upload"
              type="file"
              onChange={handleFileChange}
              style={{ display: "none" }}
            />
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            <label style={{ fontWeight: 600 }}>Target Role</label>
            <input
              style={inputStyle}
              placeholder="e.g. Machine Learning Engineer"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />

            <label style={{ fontWeight: 600 }}>Preferred Location</label>
            <select
              style={{ ...inputStyle, appearance: "none", cursor: "pointer" }}
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            >
              <option value="">Select a state</option>
              {US_STATES.map((state) => (
                <option key={state.code} value={state.name}>
                  {state.name}
                </option>
              ))}
              <option value="Remote">Remote</option>
            </select>

            <label style={{ fontWeight: 600 }}>Experience Level</label>
            <select
              style={{ ...inputStyle, appearance: "none", cursor: "pointer" }}
              value={experience}
              onChange={(e) => setExperience(e.target.value)}
            >
              <option value="0">0 years</option>
              <option value="1-3">1 - 3 years</option>
              <option value="3-5">3 - 5 years</option>
              <option value="5+">5+ years</option>
            </select>
          </div>
        </div>

        <button
          onClick={handleSubmit}
          disabled={loading}
          style={{
            marginTop: "40px",
            width: "100%",
            padding: "16px",
            fontSize: "18px",
            fontWeight: 600,
            borderRadius: "999px",
            border: "none",
            background: "linear-gradient(135deg, #2563eb 0%, #38bdf8 100%)",
            color: "#fff",
            cursor: loading ? "not-allowed" : "pointer",
            boxShadow: "0 20px 45px rgba(37, 99, 235, 0.45)",
            transition: "transform 0.2s ease"
          }}
        >
          {loading ? "Matching..." : "Search Matches"}
        </button>
      </div>
    </div>
  );
}

const inputStyle: React.CSSProperties = {
  padding: "14px 18px",
  borderRadius: "14px",
  border: "1px solid rgba(255,255,255,0.35)",
  backgroundColor: "rgba(15,23,42,0.35)",
  color: "#f8fafc",
  fontSize: "16px"
};

const US_STATES = [
  { code: "AL", name: "Alabama" },
  { code: "AK", name: "Alaska" },
  { code: "AZ", name: "Arizona" },
  { code: "AR", name: "Arkansas" },
  { code: "CA", name: "California" },
  { code: "CO", name: "Colorado" },
  { code: "CT", name: "Connecticut" },
  { code: "DE", name: "Delaware" },
  { code: "FL", name: "Florida" },
  { code: "GA", name: "Georgia" },
  { code: "HI", name: "Hawaii" },
  { code: "ID", name: "Idaho" },
  { code: "DC", name: "District of Columbia" },
  { code: "IL", name: "Illinois" },
  { code: "IN", name: "Indiana" },
  { code: "IA", name: "Iowa" },
  { code: "KS", name: "Kansas" },
  { code: "KY", name: "Kentucky" },
  { code: "LA", name: "Louisiana" },
  { code: "ME", name: "Maine" },
  { code: "MD", name: "Maryland" },
  { code: "MA", name: "Massachusetts" },
  { code: "MI", name: "Michigan" },
  { code: "MN", name: "Minnesota" },
  { code: "MS", name: "Mississippi" },
  { code: "MO", name: "Missouri" },
  { code: "MT", name: "Montana" },
  { code: "NE", name: "Nebraska" },
  { code: "NV", name: "Nevada" },
  { code: "NH", name: "New Hampshire" },
  { code: "NJ", name: "New Jersey" },
  { code: "NM", name: "New Mexico" },
  { code: "NY", name: "New York" },
  { code: "NC", name: "North Carolina" },
  { code: "ND", name: "North Dakota" },
  { code: "OH", name: "Ohio" },
  { code: "OK", name: "Oklahoma" },
  { code: "OR", name: "Oregon" },
  { code: "PA", name: "Pennsylvania" },
  { code: "RI", name: "Rhode Island" },
  { code: "SC", name: "South Carolina" },
  { code: "SD", name: "South Dakota" },
  { code: "TN", name: "Tennessee" },
  { code: "TX", name: "Texas" },
  { code: "UT", name: "Utah" },
  { code: "VT", name: "Vermont" },
  { code: "VA", name: "Virginia" },
  { code: "WA", name: "Washington" },
  { code: "WV", name: "West Virginia" },
  { code: "WI", name: "Wisconsin" },
  { code: "WY", name: "Wyoming" }
];

export default SearchPage;
