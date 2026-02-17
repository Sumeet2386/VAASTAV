import { useState } from "react";
import FileUploader from "../components/FileUploader";

export default function AudioSection() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleVerify = (response) => {
    setError(null);
    setResult(response);
  };

  return (
    <div>
      <h2>Audio Verification</h2>

   
      

      <FileUploader
        accept="audio/*"
        onVerify={handleVerify}
      />

      {error && (
        <p style={{ color: "red", marginTop: "15px" }}>
          {error}
        </p>
      )}

      {result && (
        <div
          style={{
            marginTop: "20px",
            padding: "20px",
            background: "#1f1f1f",
            borderRadius: "10px"
          }}
        >
          <p>
            <strong>Verdict:</strong> {result.verdict}
          </p>

          <p>
            <strong>Confidence:</strong> {result.confidence}%
          </p>

          {result.reasons && result.reasons.length > 0 && (
            <>
              <p><strong>Reasons:</strong></p>
              <ul>
                {result.reasons.map((reason, index) => (
                  <li key={index}>{reason}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}
