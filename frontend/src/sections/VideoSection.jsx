import { useState } from "react";
import FileUploader from "../components/FileUploader";

export default function VideoSection() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleVerify = (response) => {
    setError(null);
    setResult(response);
  };

  return (
    <div>
      <h2>Video Verification</h2>

      <FileUploader
        accept="video/*"
        onVerify={handleVerify}
      />

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div style={{ marginTop: "20px" }}>
          <p><strong>Verdict:</strong> {result.verdict}</p>
          <p><strong>Confidence:</strong> {result.confidence}%</p>
        </div>
      )}
    </div>
  );
}
