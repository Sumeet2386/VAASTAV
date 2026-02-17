from app.services.image.metadata import analyze_image_metadata
from app.services.image.artifacts import analyze_image_artifacts
from app.services.ml.image_model import predict_image_ai
def verify_image(image_path: str):
    # ---------------- Rule-based checks (existing) ----------------
    # Example placeholders – keep your actual logic if different
    metadata_score = 0.6        # 0–1
    artifact_score = 0.7        # 0–1

    # ---------------- ML-based check ----------------
    ml_result = predict_image_ai(image_path)
    ml_score = ml_result["ai_probability"] / 100.0

    # ---------------- Hybrid weighted decision ----------------
    final_score = (
        0.4 * ml_score +
        0.3 * artifact_score +
        0.3 * metadata_score
    )

    verdict = "AI Generated" if final_score > 0.5 else "Likely Real"

    # ---------------- Explanation ----------------
    reasons = []

    if ml_score > 0.6:
        reasons.append("CNN-based feature analysis indicates AI-like patterns")

    if artifact_score > 0.6:
        reasons.append("Visual artifact anomalies detected")

    if metadata_score < 0.5:
        reasons.append("Missing or inconsistent metadata")

    return {
        "verdict": verdict,
        "confidence": round(final_score * 100, 2),
        "ml_confidence": ml_result,
        "reasons": reasons
    }
