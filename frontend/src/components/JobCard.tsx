// frontend/src/components/JobCard.tsx

type JobCardProps = {
  title: string;
  company: string;
  location: string;
  score?: number;
  description: string;
};

function JobCard({ title, company, location, score, description }: JobCardProps) {
  return (
    <div style={{
      border: "1px solid #ccc",
      padding: "16px",
      borderRadius: "8px",
      marginBottom: "16px"
    }}>
      <h2>{title}</h2>
      <h3>{company}</h3>
      <p>{location}</p>
      {score !== undefined && <p>Score: {score}</p>}
      <p>{description}</p>
    </div>
  );
}

export default JobCard;
