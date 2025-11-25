// frontend/src/components/JobCard.tsx

import "../styles/jobcard.css";

type JobCardProps = {
  title: string;
  company: string;
  location: string;
  score?: number;
  description?: string;
  applyLink?: string;
  onSelect?: () => void;
};

function JobCard({
  title,
  company,
  location,
  score,
  description,
  applyLink,
  onSelect
}: JobCardProps) {
  const overview =
    description && description.length > 0
      ? `${description.slice(0, 180)}${description.length > 180 ? "..." : ""}`
      : "No company overview available.";

  return (
    <div className="jobcard-container">
      <div className="jobcard-header">
        <h2 className="jobcard-title">{title}</h2>
        <h3 className="jobcard-company">{company}</h3>
        <p className="jobcard-location">{location}</p>
        {score !== undefined && <p className="jobcard-score">Match Score: {score}</p>}
      </div>

      <div className="jobcard-overview">
        <p className="jobcard-overview-label">Company Overview</p>
        <p className="jobcard-overview-text">{overview}</p>
      </div>

      {onSelect ? (
        <button className="jobcard-button" onClick={onSelect}>
          View Details
        </button>
      ) : (
        applyLink && (
        <a
          className="jobcard-button"
          href={applyLink}
          target="_blank"
          rel="noreferrer"
        >
          View Details
        </a>
        )
      )}
    </div>
  );
}

export default JobCard;
