import filetype

def detect_file_type(file_bytes: bytes) -> str:
    """
    Detects whether the uploaded file is an image, pdf, or video.
    """
    kind = filetype.guess(file_bytes)

    if not kind:
        return "unknown"

    mime = kind.mime

    if mime.startswith("image"):
        return "image"

    if mime == "application/pdf":
        return "pdf"

    if mime.startswith("video"):
        return "video"

    return "unknown"
