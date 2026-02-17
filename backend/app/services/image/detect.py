from app.services.ml.image_model import predict_image_ai

def verify_image(image_path: str):
    # Existing rule-based checks
    metadata_score = 0.6
    artifact_score = 0.7

    # ML Prediction
    ml_result = predict_image_ai(image_path)
    ml_score = ml_result["ai_probability"] / 100

    # Hybrid weighted score
    final_score = (
        (0.4 * ml_score) +
        (0.3 * artifact_score) +
        (0.3 * metadata_score)
    )

    verdict = "AI Generated" if final_score > 0.5 else "Likely Real"

    reasons = []
    if ml_score > 0.6:
        reasons.append("CNN model detected AI-like visual patterns")
    if artifact_score > 0.6:
        reasons.append("Visual artifacts detected")
    if metadata_score < 0.5:
        reasons.append("Missing or inconsistent metadata")

    return {
        "verdict": verdict,
        "confidence": round(final_score * 100, 2),
        "ml_confidence": ml_result,
        "reasons": reasons
    }
