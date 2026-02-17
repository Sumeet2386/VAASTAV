import cv2

SUSPICIOUS_VIDEO_TOOLS = [
    "after effects",
    "premiere",
    "final cut",
    "capcut",
    "filmora"
]

def analyze_video_metadata(file_path):
    reasons = []
    score = 0.0

    cap = cv2.VideoCapture(file_path)

    if not cap.isOpened():
        reasons.append("Unable to read video file")
        return -0.3, reasons

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = frame_count / fps if fps else 0

    reasons.append(f"FPS detected: {int(fps)}")
    reasons.append(f"Duration: {round(duration, 2)} seconds")

    if fps < 10 or fps > 60:
        reasons.append("Unusual frame rate detected")
        score -= 0.1
    else:
        score += 0.1

    cap.release()
    return score, reasons
