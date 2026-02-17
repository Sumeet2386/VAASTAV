from PIL import Image

SUSPICIOUS_TOOLS = [
    "photoshop", "gimp", "canva",
    "snapseed", "editor", "paint"
]

def analyze_image_metadata(file):
    reasons = []
    score = 0.0

    try:
        image = Image.open(file.file)
        metadata = image.info or {}

        software = str(metadata.get("Software", "")).lower()
        if software:
            reasons.append(f"Image created using: {software}")
            if any(tool in software for tool in SUSPICIOUS_TOOLS):
                reasons.append("Image shows signs of manual editing")
                score -= 0.2
            else:
                score += 0.1
        else:
            reasons.append("No software metadata found")

    except Exception:
        reasons.append("Unable to read image metadata")

    return score, reasons
