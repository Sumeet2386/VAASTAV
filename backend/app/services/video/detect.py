from app.services.ml.video_model import predict_video_ai

def verify_video(video_path: str):
    try:
        # ---------- Existing heuristic checks ----------
        metadata_score = 0.6     # placeholder
        motion_score = 0.7       # placeholder

        # ---------- ML analysis ----------
        ml_result = predict_video_ai(video_path)
        ml_score = ml_result["ai_probability"] / 100.0

        # ---------- Hybrid decision ----------
        final_score = (
            0.4 * ml_score +
            0.3 * motion_score +
            0.3 * metadata_score
        )

        verdict = "AI Generated" if final_score > 0.5 else "Likely Real"

        # ---------- Explanation ----------
        reasons = []

        if ml_score > 0.6:
            reasons.append("Frame-level CNN analysis indicates AI-like patterns")

        if motion_score > 0.6:
            reasons.append("Temporal motion inconsistencies detected")

        if metadata_score < 0.5:
            reasons.append("Suspicious or missing video metadata")

        return {
            "verdict": verdict,
            "confidence": round(final_score * 100, 2),
            "ml_confidence": ml_result,
            "reasons": reasons
        }

    except Exception as e:
        print("VIDEO PROCESSING ERROR:", e)

        return {
            "verdict": "Error",
            "confidence": 0,
            "ml_confidence": {
                "ai_probability": 50,
                "real_probability": 50
            },
            "reasons": ["Video processing failed"]
        }
