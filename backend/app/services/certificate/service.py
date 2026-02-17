from app.services.certificate.ocr import extract_text_from_image

from app.services.certificate.qr import detect_qr_from_certificate
from app.services.certificate.metadata import analyze_metadata
from app.services.certificate.decision import make_decision

async def verify_certificate(file_bytes: bytes, filename: str, content_type: str):
    from app.services.certificate.ocr import extract_text_from_image
    from app.services.certificate.qr import detect_qr_from_certificate
    from app.services.certificate.metadata import analyze_metadata
    from app.services.certificate.decision import make_decision

    ocr_text = extract_text_from_image(file_bytes)
    qr_detected = detect_qr_from_certificate(file_bytes)
    metadata = analyze_metadata(file_bytes)

    decision = make_decision(
        ocr_text=ocr_text,
        qr_detected=qr_detected,
        metadata=metadata
    )

    return {
        "status": "RECEIVED",
        "filename": filename,
        "routing": {
            "mediaType": "image",
            "analysis": {
                "ocr_text": ocr_text,
                "qr_detected": qr_detected,
                "metadata": metadata
            },
            "decision": decision
        }
    }


    return {
        "status": "RECEIVED",
        "filename": filename,
        "routing": {
            "mediaType": "image",
            "analysis": {
                "ocr_text": ocr_text,
                "qr_detected": qr_detected,
                "metadata": metadata
            },
            "decision": decision
        }
    }
