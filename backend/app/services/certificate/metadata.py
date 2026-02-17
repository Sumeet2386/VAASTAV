from PIL import Image

SUSPICIOUS_CREATORS = [
    "photoshop",
    "gimp",
    "canva",
    "editor",
    "paint",
    "snapseed"
]

def extract_metadata(file):
    try:
        image = Image.open(file.file)
        return image.info or {}
    except Exception:
        return {}

def analyze_metadata(file_bytes: bytes):
    # Placeholder for EXIF / metadata checks
    return {
        "has_metadata": False,
        "suspicious_fields": []
    }


