// frontend/src/pages/LandingPage.tsx

import { useNavigate } from "react-router-dom";

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: "40px", textAlign: "center" }}>
      <h1>Welcome to Resume Recommender</h1>
      <p>Upload your resume and get job recommendations powered by NLP.</p>

      <button
        onClick={() => navigate("/feed")}
        style={{
          padding: "12px 24px",
          fontSize: "18px",
          marginTop: "20px",
          cursor: "pointer"
        }}
      >
        Start
      </button>
    </div>
  );
}

export default LandingPage;
