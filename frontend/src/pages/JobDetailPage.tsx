// frontend/src/pages/JobDetailPage.tsx

import { useLocation, useNavigate } from "react-router-dom";
import JobDetailCard, { JobDetail } from "../components/JobDetailCard";

function JobDetailPage() {
  const navigate = useNavigate();
  const locationState = useLocation();
  const job = locationState.state?.job as JobDetail | undefined;

  if (!job) {
    return (
      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background:
            "radial-gradient(circle at top, #4f7ccf 0%, #1b2b5a 55%, #0a1024 100%)",
          color: "#fff",
        }}
      >
        <div
          style={{
            padding: "40px",
            borderRadius: "24px",
            backgroundColor: "rgba(255,255,255,0.08)",
            backdropFilter: "blur(10px)",
            textAlign: "center",
            maxWidth: "480px",
          }}
        >
          <h1 style={{ marginBottom: "12px" }}>Job Details</h1>
          <p style={{ marginBottom: "24px" }}>No job selected. Please return to the results list.</p>
          <button
            onClick={() => navigate("/result")}
            style={{
              padding: "12px 24px",
              borderRadius: "999px",
              border: "none",
              background: "linear-gradient(135deg, #2563eb 0%, #38bdf8 100%)",
              color: "#fff",
              cursor: "pointer",
            }}
          >
            Back to Results
          </button>
        </div>
      </div>
    );
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100%",
        padding: "48px 24px",
        background:
          "radial-gradient(circle at top, #4f7ccf 0%, #1b2b5a 55%, #0a1024 100%)",
        boxSizing: "border-box",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <JobDetailCard job={job} onClose={() => navigate(-1)} />
    </div>
  );
}

export default JobDetailPage;
