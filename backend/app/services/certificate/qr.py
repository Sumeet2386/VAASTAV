from pyzbar.pyzbar import decode
from PIL import Image
import io
import numpy as np

def detect_qr_from_certificate(file):
    try:
        image_bytes = file.file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_np = np.array(image)

        qr_codes = decode(image_np)

        results = []
        for qr in qr_codes:
            results.append(qr.data.decode("utf-8"))

        return results

    except Exception:
        return []
