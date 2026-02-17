import { verifyCertificate } from "../services/api";

const handleVerify = async () => {
  try {
    const result = await verifyCertificate(selectedFile);
    setResult(result);
    setError(null);
  } catch (err) {
    setError("Backend not reachable");
  }
};
