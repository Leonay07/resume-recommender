// frontend/src/components/JobDetailCard.tsx

export type JobDetail = {
  title: string;
  company: string;
  location: string;
  description: string;
  apply_link?: string;
  score?: number;
  summary?: string;
  evidence_image?: string;
  keywords?: string[];
};

type JobDetailCardProps = {
  job: JobDetail;
  onClose?: () => void;
};

function normalizeScore(score?: number) {
  if (typeof score !== "number") return null;
  if (score > 1) return Math.round(score);
  return Math.round(score * 100);
}

function formatParagraphs(text?: string) {
  if (!text) return [];
  return text
    .split(/\n+/)
    .map((block) => block.trim())
    .filter(Boolean);
}

function formatSummary(text?: string) {
  if (!text) return [];
  return text
    .split(/(?<=\.)\s+/)
    .map((sentence) => sentence.trim())
    .filter(Boolean);
}

function JobDetailCard({ job, onClose }: JobDetailCardProps) {
  const normalizedScore = normalizeScore(job.score);
  const descriptionBlocks = formatParagraphs(job.description);
  const summarySentences = formatSummary(job.summary);
  const evidenceImage = typeof job.evidence_image === "string" ? job.evidence_image : null;

  return (
    <div
      style={{
        width: "min(960px, 100%)",
        background: "linear-gradient(135deg, rgba(255,255,255,0.1), rgba(15,23,42,0.55))",
        borderRadius: "32px",
        border: "1px solid rgba(255, 255, 255, 0.18)",
        padding: "48px",
        boxShadow: "0 35px 90px rgba(5,10,25,0.45)",
        color: "#f8fafc",
        backdropFilter: "blur(14px)",
        maxHeight: "90vh",
        overflowY: "auto",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "24px",
          gap: "16px",
        }}
      >
        <div>
          <p
            style={{
              textTransform: "uppercase",
              letterSpacing: "0.2em",
              fontSize: "13px",
              color: "rgba(226,232,240,0.8)",
              margin: "0 0 12px",
            }}
          >
            Recommended Role
          </p>
          <h1 style={{ margin: "0 0 8px" }}>{job.title}</h1>
          <h2 style={{ margin: "0 0 8px", color: "rgba(248,250,252,0.85)" }}>
            {job.company}
          </h2>
          <p style={{ margin: 0, color: "rgba(226,232,240,0.7)" }}>{job.location}</p>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            style={{
              width: "42px",
              height: "42px",
              borderRadius: "50%",
              border: "1px solid rgba(255,255,255,0.25)",
              backgroundColor: "rgba(255,255,255,0.08)",
              color: "#f8fafc",
              cursor: "pointer",
              fontSize: "18px",
            }}
          >
            ×
          </button>
        )}
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
          gap: "24px",
          marginBottom: "32px",
        }}
      >
        {normalizedScore !== null && (
          <div
            style={{
              padding: "20px",
              borderRadius: "18px",
              backgroundColor: "rgba(15,23,42,0.55)",
              border: "1px solid rgba(99,102,241,0.4)",
            }}
          >
            <span style={{ fontSize: "14px", color: "rgba(226,232,240,0.8)" }}>
              Match Score
            </span>
            <h3 style={{ margin: "8px 0 0", fontSize: "32px", color: "#c7d2fe" }}>
              {normalizedScore}%
            </h3>
          </div>
        )}

        <div
          style={{
            padding: "24px",
            borderRadius: "24px",
            backgroundColor: "rgba(8,12,28,0.45)",
            border: "1px solid rgba(255,255,255,0.08)",
          }}
        >
          <h3 style={{ marginTop: 0, marginBottom: "12px" }}>Match Summary</h3>
          {summarySentences.length > 0 ? (
            <ul style={{ paddingLeft: "18px", margin: 0, lineHeight: 1.6 }}>
              {summarySentences.map((sentence, idx) => (
                <li key={idx}>{sentence}</li>
              ))}
            </ul>
          ) : (
            <p style={{ margin: 0, color: "rgba(226,232,240,0.75)" }}>
              No summary provided by the model.
            </p>
          )}
        </div>
      </div>

      {Array.isArray(job.keywords) && job.keywords.length > 0 && (
        <div style={{ marginBottom: "32px" }}>
          <p style={{ marginBottom: "12px", fontWeight: 600 }}>Highlighted Skills</p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "10px" }}>
            {job.keywords.map((keyword, idx) => (
              <span
                key={idx}
                style={{
                  padding: "8px 14px",
                  borderRadius: "999px",
                  backgroundColor: "rgba(15,23,42,0.6)",
                  border: "1px solid rgba(148,163,184,0.4)",
                  fontSize: "14px",
                }}
              >
                {keyword}
              </span>
            ))}
          </div>
        </div>
      )}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: evidenceImage ? "2fr 1fr" : "1fr",
          gap: "24px",
          alignItems: "flex-start",
        }}
      >
        <div
          style={{
            backgroundColor: "rgba(8,12,28,0.45)",
            borderRadius: "24px",
            padding: "28px",
            border: "1px solid rgba(255,255,255,0.08)",
          }}
        >
          <h3 style={{ marginTop: 0, marginBottom: "12px" }}>Company Overview</h3>
          {descriptionBlocks.length > 0 ? (
            <div style={{ lineHeight: 1.8, color: "rgba(226,232,240,0.9)" }}>
              {descriptionBlocks.map((block, idx) => (
                <p key={idx} style={{ marginTop: idx === 0 ? 0 : "16px" }}>
                  {block}
                </p>
              ))}
            </div>
          ) : (
            <p>No description available.</p>
          )}
        </div>

        {evidenceImage && (
          <div
            style={{
              backgroundColor: "rgba(8,12,28,0.45)",
              borderRadius: "24px",
              padding: "20px",
              border: "1px solid rgba(255,255,255,0.08)",
              textAlign: "center",
            }}
          >
            <h3 style={{ marginTop: 0, marginBottom: "12px" }}>Model Evidence</h3>
            <img
              src={evidenceImage}
              alt="Model explanation"
              style={{
                maxWidth: "100%",
                borderRadius: "18px",
                border: "1px solid rgba(255,255,255,0.15)",
                backgroundColor: "#fff",
              }}
            />
          </div>
        )}
      </div>

      {job.apply_link && (
        <a
          href={job.apply_link}
          target="_blank"
          rel="noreferrer"
          style={{
            display: "block",
            marginTop: "36px",
            width: "100%",
            textAlign: "center",
            padding: "16px",
            borderRadius: "999px",
            background: "linear-gradient(135deg, #22d3ee, #4f46e5)",
            color: "#fff",
            fontWeight: 600,
            textDecoration: "none",
          }}
        >
          Apply on Company Site
        </a>
      )}
    </div>
  );
}

export default JobDetailCard;
