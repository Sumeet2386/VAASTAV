import tempfile
import shutil

from app.services.video.metadata import analyze_video_metadata
from app.services.video.frames import analyze_frame_consistency

async def verify_video(file):
    reasons = []
    score = 0.5  # neutral baseline

    # Save temporarily (required for cv2)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    meta_score, meta_reasons = analyze_video_metadata(tmp_path)
    frame_score, frame_reasons = analyze_frame_consistency(tmp_path)

    score += meta_score + frame_score
    reasons.extend(meta_reasons + frame_reasons)

    if score >= 0.7:
        status = "LIKELY_GENUINE"
    elif score >= 0.4:
        status = "INCONCLUSIVE"
    else:
        status = "LIKELY_MANIPULATED"

    return {
        "mediaType": "Video",
        "decision": {
            "status": status,
            "confidence": round(score, 2),
            "reasons": reasons
        }
    }
