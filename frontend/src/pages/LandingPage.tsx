// frontend/src/pages/LandingPage.tsx

import { useNavigate } from "react-router-dom";

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "48px 24px",
        boxSizing: "border-box",
        background:
          "radial-gradient(circle at top, rgba(79, 124, 207, 0.9), rgba(15, 27, 50, 0.95))",
        color: "#ffffff"
      }}
    >
      <div
        style={{
          width: "min(1100px, 100%)",
          padding: "64px 56px",
          borderRadius: "32px",
          background:
            "linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05))",
          border: "1px solid rgba(255, 255, 255, 0.25)",
          boxShadow: "0 40px 100px rgba(0, 0, 0, 0.35)",
          textAlign: "center",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: "24px"
        }}
      >
        <p
          style={{
            fontSize: "15px",
            fontWeight: 600,
            letterSpacing: "0.25em",
            textTransform: "uppercase",
            margin: 0,
            color: "rgba(255, 255, 255, 0.8)"
          }}
        >
          Resume Recommender
        </p>
        <h1
          style={{
            fontSize: "54px",
            lineHeight: 1.2,
            margin: 0
          }}
        >
          Personalized Job Matches Start Here
        </h1>
        <p
          style={{
            fontSize: "20px",
            maxWidth: "720px",
            margin: 0,
            opacity: 0.9
          }}
        >
        Upload your resume and target roles, and let our NLP-powered machine learning engine automatically surface the opportunities that best match your profile and long-term goals.
        </p>
        <button
          onClick={() => navigate("/feed", { state: { refresh: true } })}
          style={{
            padding: "16px 48px",
            fontSize: "20px",
            fontWeight: 600,
            borderRadius: "32px",
            border: "none",
            background: "#ffffff",
            color: "#1f3b73",
            cursor: "pointer",
            boxShadow: "0 20px 45px rgba(15, 27, 50, 0.4)",
            transition: "transform 0.2s ease, box-shadow 0.2s ease"
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = "translateY(-3px)";
            e.currentTarget.style.boxShadow =
              "0 28px 55px rgba(15, 27, 50, 0.5)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = "translateY(0)";
            e.currentTarget.style.boxShadow =
              "0 20px 45px rgba(15, 27, 50, 0.4)";
          }}
        >
          Get Started
        </button>
        <p
          style={{
            marginTop: "16px",
            opacity: 0.85,
            fontSize: "16px",
            letterSpacing: "0.08em"
          }}
        >
          Group 8 · Liming · Yuang · Yiran · Renke · Siyu 
        </p>
      </div>
    </div>
  );
}

export default LandingPage;
