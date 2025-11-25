// frontend/src/pages/ResultPage.tsx
// Display matched jobs + load more results from /match/more

import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import JobCard from "../components/JobCard";
import JobDetailCard from "../components/JobDetailCard";
import { getMoreJobs } from "../api/apiClient";

interface JobItem {
  title: string;
  company: string;
  location: string;
  description: string;
  apply_link: string;
  score?: number;
  summary?: string;
  evidence_image?: string;
  [key: string]: unknown;
}

function ResultPage() {
  const navigate = useNavigate();

  const locationState = useLocation();
  const initialResults: JobItem[] = locationState.state?.results || [];

  const [jobs, setJobs] = useState<JobItem[]>(initialResults);
  const [loadingMore, setLoadingMore] = useState(false);
  const [selectedJob, setSelectedJob] = useState<JobItem | null>(null);

  const handleLoadMore = async () => {
    setLoadingMore(true);
    const moreJobs: JobItem[] = await getMoreJobs();

    const uniqueJobs: JobItem[] = [
      ...jobs,
      ...moreJobs.filter(
        (job: JobItem) =>
          !jobs.some(
            (j: JobItem) =>
              j.title === job.title && j.company === job.company
          )
      ),
    ];

    setJobs(uniqueJobs);
    setLoadingMore(false);
  };

  if (!locationState.state) {
    return (
      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background:
            "radial-gradient(circle at top, #4f7ccf 0%, #1b2b5a 55%, #0a1024 100%)",
          color: "#fff"
        }}
      >
        <div
          style={{
            padding: "40px",
            borderRadius: "24px",
            backgroundColor: "rgba(255,255,255,0.08)",
            backdropFilter: "blur(10px)",
            textAlign: "center",
            maxWidth: "480px"
          }}
        >
          <h1 style={{ marginBottom: "12px" }}>Match Results</h1>
          <p style={{ marginBottom: "24px" }}>
            No search data detected. Please return to the search page.
          </p>
          <button
            onClick={() => navigate("/search")}
            style={{
              padding: "12px 24px",
              borderRadius: "999px",
              border: "none",
              background: "linear-gradient(135deg, #2563eb 0%, #38bdf8 100%)",
              color: "#fff",
              cursor: "pointer"
            }}
          >
            Back to Search
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
        background:
          "radial-gradient(circle at top, #4f7ccf 0%, #1b2b5a 55%, #0a1024 100%)",
        padding: "60px 24px",
        boxSizing: "border-box"
      }}
    >
      <div
        style={{
          maxWidth: "960px",
          margin: "0 auto",
          background:
            "linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.04))",
          borderRadius: "28px",
          border: "1px solid rgba(255,255,255,0.15)",
          padding: "48px",
          color: "#f8fafc",
          boxShadow: "0 30px 70px rgba(7, 12, 28, 0.45)"
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
          Match Results
        </p>
        <h1 style={{ margin: "0 0 32px" }}>Here are your top recommendations</h1>

        {jobs.length === 0 && (
          <p style={{ marginBottom: "24px", color: "rgba(226,232,240,0.8)" }}>
            No matched jobs found. Try another search.
          </p>
        )}

        <div style={{ display: "flex", flexDirection: "column", gap: "18px" }}>
          {jobs.map((job, index) => (
            <JobCard
              key={`${job.title}-${job.company}-${index}`}
              title={job.title}
              company={job.company}
              location={job.location}
              score={job.score}
              description={job.description}
              onSelect={() => setSelectedJob(job)}
            />
          ))}
        </div>

        <button
          onClick={handleLoadMore}
          disabled={loadingMore}
          style={{
            marginTop: "32px",
            width: "100%",
            padding: "16px",
            borderRadius: "999px",
            border: "none",
            background: "linear-gradient(135deg, #0ea5e9, #6366f1)",
            color: "#fff",
            fontSize: "16px",
            fontWeight: 600,
            cursor: loadingMore ? "not-allowed" : "pointer",
            opacity: loadingMore ? 0.7 : 1
          }}
        >
          {loadingMore ? "Loading..." : "Load More"}
        </button>
      </div>
      {selectedJob && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            background: "rgba(5, 10, 25, 0.75)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            padding: "24px",
            boxSizing: "border-box",
            zIndex: 1000,
          }}
        >
          <JobDetailCard job={selectedJob} onClose={() => setSelectedJob(null)} />
        </div>
      )}
    </div>
  );
}

export default ResultPage;
