import { useState } from "react";
import FileUploader from "../components/FileUploader";

export default function ImageSection() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleVerify = (response) => {
    setError(null);
    setResult(response);
  };

  return (
    <div>
      <h2>Image Verification</h2>

      <FileUploader
        accept="image/*"
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
