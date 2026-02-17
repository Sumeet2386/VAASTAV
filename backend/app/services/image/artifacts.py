from PIL import Image

def analyze_image_artifacts(file):
    reasons = []
    score = 0.0

    try:
        image = Image.open(file.file)
        width, height = image.size

        if width < 300 or height < 300:
            reasons.append("Low resolution image detected")
            score -= 0.2
        else:
            reasons.append("Image resolution appears normal")
            score += 0.1

        if image.format == "JPEG":
            reasons.append("JPEG compression detected (common for edited images)")
            score -= 0.05

    except Exception:
        reasons.append("Unable to analyze image artifacts")

    return score, reasons
