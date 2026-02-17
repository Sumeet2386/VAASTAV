from app.services.detect_media import detect_media_type
from app.services.certificate_service import verify_certificate
from app.services.image_service import verify_image
from app.services.video_service import verify_video

async def route_media(file):
    media_type = detect_media_type(file.filename)

    if media_type == "certificate":
        return await verify_certificate(file)
    elif media_type == "image":
        return await verify_image(file)
    elif media_type == "video":
        return await verify_video(file)
    else:
        return {
            "status": "failed",
            "media_type": "unknown",
            "confidence_score": 0
        }
