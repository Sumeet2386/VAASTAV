from app.services.certificate.certificate_model import verify_certificate

def process_certificate(file_path: str):
    return verify_certificate(file_path)
