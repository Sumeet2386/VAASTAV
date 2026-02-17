def make_verdict(confidence: int):
    if confidence >= 80:
        return "AUTHENTIC"
    if confidence >= 50:
        return "SUSPICIOUS"
    return "NOT_VERIFIED"
