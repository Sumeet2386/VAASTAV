import cv2
import numpy as np

def analyze_frame_consistency(file_path):
    reasons = []
    score = 0.0

    cap = cv2.VideoCapture(file_path)
    prev_frame = None
    jumps = 0
    checked = 0

    while cap.isOpened() and checked < 10:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is not None:
            diff = np.mean(cv2.absdiff(prev_frame, gray))
            if diff > 40:
                jumps += 1

        prev_frame = gray
        checked += 1

    cap.release()

    if jumps > 3:
        reasons.append("High frame inconsistency detected")
        score -= 0.2
    else:
        reasons.append("Frame consistency appears normal")
        score += 0.2

    return score, reasons
