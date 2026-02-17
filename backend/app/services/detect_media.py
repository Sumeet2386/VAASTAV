def detect_media_type(filename: str) -> str:
    ext = filename.lower().split(".")[-1]

    if ext in ["pdf", "png", "jpg", "jpeg"]:
        return "certificate"
    if ext in ["jpg", "jpeg", "png", "webp"]:
        return "image"
    if ext in ["mp4", "mov", "avi"]:
        return "video"

    return "unknown"
