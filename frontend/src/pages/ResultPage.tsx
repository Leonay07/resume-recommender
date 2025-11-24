// frontend/src/pages/ResultPage.tsx
// Display matched jobs + load more results from /match/more

import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import JobCard from "../components/JobCard";
import { getMoreJobs } from "../api/apiClient";

interface JobItem {
  title: string;
  company: string;
  location: string;
  description: string;
  apply_link: string;
  score?: number;
}

function ResultPage() {
  const navigate = useNavigate();

  // Receive initial 10 results passed from SearchPage
  const locationState = useLocation();
  const initialResults: JobItem[] = locationState.state?.results || [];

  // Local state for all results (initial + more)
  const [jobs, setJobs] = useState<JobItem[]>(initialResults);
  const [loadingMore, setLoadingMore] = useState(false);

  // Handle Load More button → fetch /match/more
  const handleLoadMore = async () => {
    setLoadingMore(true);

    const moreJobs: JobItem[] = await getMoreJobs(); // fetch all from cache.json

    // Merge without duplicates
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

  // If user refreshed page → no state → tell them to search again
  if (!locationState.state) {
    return (
      <div style={{ padding: "20px" }}>
        <h1>Match Results</h1>
        <p>No search data detected. Please search again.</p>
        <button
          onClick={() => navigate("/search")}
          style={{ marginTop: "16px", padding: "10px 20px" }}
        >
          Back to Search
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Match Results</h1>

      {jobs.length === 0 && <p>No matched jobs found. Try another search.</p>}

      {/* Display job cards */}
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

      {/* Load More Button */}
      <button
        onClick={handleLoadMore}
        disabled={loadingMore}
        style={{
          padding: "12px 20px",
          fontSize: "16px",
          marginTop: "20px",
          cursor: "pointer",
        }}
      >
        {loadingMore ? "Loading..." : "Load More"}
      </button>
    </div>
  );
}

export default ResultPage;
