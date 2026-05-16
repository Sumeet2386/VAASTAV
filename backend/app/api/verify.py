from fastapi import APIRouter, UploadFile, File
from app.services.image.detect import verify_image
from app.services.video.detect import verify_video
from app.services.certificate.detect import process_certificate
from app.services.audio.detect import verify_audio
import os
from pathlib import Path

router = APIRouter()

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


def secure_filename(filename: str) -> str:
    # Remove any path traversal characters
    return os.path.basename(filename)


# ================= IMAGE =================
@router.post("/image")
async def verify_image_api(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            return {"status": "error", "message": "Invalid file type"}

        safe_filename = secure_filename(file.filename)
        file_path = Path(TEMP_DIR) / safe_filename
        with open(file_path, "wb") as f:
            f.write(await file.read())

        result = verify_image(str(file_path))

        return {
            "status": "success",
            "verdict": result.get("verdict"),
            "confidence": result.get("confidence"),
            "ml_confidence": result.get("ml_confidence"),
            "reasons": result.get("reasons", [])
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# ================= VIDEO =================
@router.post("/video")
async def verify_video_api(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("video/"):
            return {"status": "error", "message": "Invalid file type"}

        safe_filename = secure_filename(file.filename)
        file_path = Path(TEMP_DIR) / safe_filename
        with open(file_path, "wb") as f:
            f.write(await file.read())

        result = verify_video(str(file_path))

        return {
            "status": "success",
            "verdict": result.get("verdict"),
            "confidence": result.get("confidence"),
            "ml_confidence": result.get("ml_confidence"),
            "reasons": result.get("reasons", [])
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# ================= CERTIFICATE =================
@router.post("/certificate")
async def verify_certificate_api(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith(("image/", "application/pdf")):
            return {"status": "error", "message": "Invalid certificate format"}

        safe_filename = secure_filename(file.filename)
        file_path = Path(TEMP_DIR) / safe_filename
        with open(file_path, "wb") as f:
            f.write(await file.read())

        result = process_certificate(str(file_path))

        return {
            "status": "success",
            "verdict": result.get("verdict"),
            "certificate_confidence": result.get("certificate_confidence"),
            "name_integrity_confidence": result.get("name_integrity_confidence"),
            "name_detected": result.get("name_detected"),
            "roll_number": result.get("roll_number"),
            "qr_data": result.get("qr_data"),
            "reasons": result.get("reasons", [])
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# ================= AUDIO =================
@router.post("/audio")
async def verify_audio_api(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("audio/"):
            return {"status": "error", "message": "Invalid audio file"}

        safe_filename = secure_filename(file.filename)
        file_path = Path(TEMP_DIR) / safe_filename
        with open(file_path, "wb") as f:
            f.write(await file.read())

        result = verify_audio(str(file_path))

        # If your model already returns correct keys
        return result

    except Exception as e:
        return {"status": "error", "message": str(e)}
