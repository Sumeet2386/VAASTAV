import { useState } from "react";

export default function FileUploader({ onVerify, accept }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const detectEndpoint = (file) => {
    if (!file) return null;

    if (file.type.startsWith("image/")) return "image";
    if (file.type.startsWith("video/")) return "video";
    if (file.type.startsWith("audio/")) return "audio";
    if (file.type === "application/pdf") return "certificate";

    return "certificate";
  };

  const handleVerifyClick = async () => {
    if (!file) {
      alert("Please select a file first");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const endpoint = detectEndpoint(file);

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        `http://127.0.0.1:8000/api/${endpoint}`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        console.error("Backend error:", data);
        throw new Error(data.message || "Verification failed");
      }

      console.log("Backend response:", data);

      if (onVerify) {
        onVerify(data);
      }

    } catch (err) {
      console.error(err);
      setError(err.message || "Verification failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "20px", textAlign: "left" }}>
      <input
        type="file"
        accept={accept}
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br />
      <br />

      <button
        onClick={handleVerifyClick}
        disabled={loading}
        style={{
          padding: "10px 20px",
          cursor: loading ? "not-allowed" : "pointer",
        }}
      >
        {loading ? "Verifying..." : "Verify"}
      </button>

      {error && (
        <p style={{ color: "red", marginTop: "10px" }}>
          {error}
        </p>
      )}
    </div>
  );
}
