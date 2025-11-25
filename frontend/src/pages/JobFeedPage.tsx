// frontend/src/pages/JobFeedPage.tsx
// Fetch and display random jobs from backend

import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { getRandomJobs } from "../api/apiClient";
import JobCard from "../components/JobCard";
import "../styles/jobfeed.css";

// --- Job type ---
interface JobItem {
  title: string;
  company: string;
  location: string;
  description: string;
  apply_link: string;
  score?: number;
}

function JobFeedPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [jobs, setJobs] = useState<JobItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [lastRefresh, setLastRefresh] = useState<number | null>(null);
  const [cooldown, setCooldown] = useState(0);

  const CACHE_KEY = "jobFeedCache";
  const LAST_REFRESH_KEY = "jobFeedLastRefresh";
  const REFRESH_COOLDOWN_MS = 60 * 1000;

  const loadCachedJobs = (): JobItem[] | null => {
    if (typeof window === "undefined") return null;
    try {
      const cached = localStorage.getItem(CACHE_KEY);
      return cached ? JSON.parse(cached) : null;
    } catch {
      return null;
    }
  };

  const saveJobsToCache = (data: JobItem[]) => {
    if (typeof window === "undefined") return;
    localStorage.setItem(CACHE_KEY, JSON.stringify(data));
  };

  const loadLastRefresh = (): number | null => {
    if (typeof window === "undefined") return null;
    const raw = localStorage.getItem(LAST_REFRESH_KEY);
    if (!raw) return null;
    const parsed = Number(raw);
    return Number.isNaN(parsed) ? null : parsed;
  };

  const saveLastRefresh = (timestamp: number) => {
    if (typeof window === "undefined") return;
    localStorage.setItem(LAST_REFRESH_KEY, String(timestamp));
  };

  const fetchAndStoreJobs = async (force = false) => {
    if (!force && lastRefresh && Date.now() - lastRefresh < REFRESH_COOLDOWN_MS) {
      return;
    }
    setLoading(true);
    const data = await getRandomJobs();
    setJobs(data);
    saveJobsToCache(data);
    const now = Date.now();
    setLastRefresh(now);
    saveLastRefresh(now);
    setLoading(false);
  };

  useEffect(() => {
    const storedLastRefresh = loadLastRefresh();
    if (storedLastRefresh) {
      setLastRefresh(storedLastRefresh);
    }
  }, []);

  useEffect(() => {
    if (!lastRefresh) {
      setCooldown(0);
      return;
    }

    const updateCooldown = () => {
      const elapsed = Date.now() - lastRefresh;
      const remaining = Math.max(0, Math.ceil((REFRESH_COOLDOWN_MS - elapsed) / 1000));
      setCooldown(remaining);
    };

    updateCooldown();
    const interval = window.setInterval(updateCooldown, 1000);
    return () => window.clearInterval(interval);
  }, [lastRefresh]);

  useEffect(() => {
    const shouldRefresh = Boolean(location.state?.refresh);

    if (shouldRefresh) {
      fetchAndStoreJobs(true);
      navigate(".", { replace: true, state: {} });
      return;
    }

    const cached = loadCachedJobs();
    if (cached && cached.length > 0) {
      setJobs(cached);
    } else {
      fetchAndStoreJobs(true);
    }
  }, [location.state, navigate]);

  const handleRefresh = () => {
    if (loading || cooldown > 0) {
      return;
    }
    fetchAndStoreJobs(true);
  };

  return (
    <div className="jobfeed-container">
      <div className="jobfeed-content">
        <h1 className="jobfeed-title">Job Feed</h1>

        <div className="jobfeed-cta">
          <button className="jobfeed-button" onClick={() => navigate("/search")}>
            Get Customized Job
          </button>
        </div>

        <div className="jobfeed-list-header">
          <p className="jobfeed-subtitle">Current roles refreshed from our feed</p>
          <button
            className="jobfeed-refresh"
            onClick={handleRefresh}
            disabled={loading || cooldown > 0}
          >
            {loading
              ? "Refreshing..."
              : cooldown > 0
                ? `Available in ${cooldown}s`
                : "Refresh Feed"}
          </button>
        </div>

        {jobs.length === 0 && (
          <p className="loading-text">{loading ? "Loading jobs..." : "No jobs cached yet."}</p>
        )}

        <div className="job-list">
          {jobs.map((job, index) => (
            <JobCard
              key={index}
              title={job.title}
              company={job.company}
              location={job.location}
              score={job.score}
              description={job.description}
              applyLink={job.apply_link}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

export default JobFeedPage;
