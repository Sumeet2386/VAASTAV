def make_decision(ocr_text: str, qr_detected: bool, metadata: dict):
    confidence = 0.0
    reasons = []

    if ocr_text:
        confidence += 0.3
        reasons.append("Readable text extracted")

    if qr_detected:
        confidence += 0.4
        reasons.append("QR code detected")

    if not metadata.get("suspicious_fields"):
        confidence += 0.3

    status = "VERIFIED" if confidence >= 0.7 else "NOT_VERIFIED"

    return {
        "status": status,
        "confidence": round(confidence, 2),
        "reasons": reasons
    }
