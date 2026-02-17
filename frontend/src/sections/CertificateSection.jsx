import { useState } from "react";
import FileUploader from "../components/FileUploader";

export default function CertificateSection() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleVerify = (response) => {
    setError(null);
    setResult(response);
  };

  return (
    <div>
      <h2>Certificate Verification</h2>

      <FileUploader
        accept=".pdf,image/*"
        onVerify={handleVerify}
      />

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div style={{ marginTop: "20px" }}>
          <p><strong>Status:</strong> {result.status}</p>
          <p><strong>Verdict:</strong> {result.verdict}</p>
          <p><strong>Certificate Confidence:</strong> {result.certificate_confidence}%</p>
          <p><strong>Name Integrity:</strong> {result.name_integrity_confidence}%</p>
        </div>
      )}
    </div>
  );
}
