export default function ResultCard({ result }) {
  if (!result) return null;

  let color = "red";
  if (result.confidence_score >= 80) color = "green";
  else if (result.confidence_score >= 50) color = "orange";

  return (
    <div style={{ marginTop: "20px", padding: "16px", border: "1px solid #333" }}>
      <h3>Verification Result</h3>

      <p>
        <strong>Type:</strong> {result.media_type}
      </p>

      <p>
        <strong>Status:</strong>{" "}
        <span style={{ color }}>{result.status}</span>
      </p>

      <p>
        <strong>Confidence:</strong>{" "}
        <span style={{ color }}>
          {result.confidence_score}%
        </span>
      </p>
    </div>
  );
}
