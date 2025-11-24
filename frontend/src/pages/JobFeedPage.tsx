// frontend/src/pages/JobFeedPage.tsx
// Fetch and display random jobs from backend

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getRandomJobs } from "../api/apiClient";
import JobCard from "../components/JobCard";

// --- Add type definition here ---
interface JobItem {
  title: string;
  company: string;
  location: string;
  description: string;
  apply_link: string;
  score?: number;  // optional for random feed
}

function JobFeedPage() {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState<JobItem[]>([]);

  useEffect(() => {
    async function fetchData() {
      const data = await getRandomJobs();
      console.log("🔥 /jobs/random returned:", data);
      setJobs(data);
    }
    fetchData();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Job Feed</h1>

      {/* Keep your button */}
      <button
        onClick={() => navigate("/search")}
        style={{
          padding: "10px 20px",
          margin: "16px 0",
          cursor: "pointer",
          fontSize: "16px"
        }}
      >
        Get Customized Job
      </button>

      {jobs.length === 0 && <p>Loading jobs...</p>}

      {jobs.map((job, index) => (
        <JobCard
          key={index}
          title={job.title}
          company={job.company}
          location={job.location}
          score={job.score}
          description={job.description}
        />
      ))}
    </div>
  );
}

export default JobFeedPage;
