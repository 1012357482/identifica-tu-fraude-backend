import io
import hashlib
from PIL import Image

# Intentar importar pyzbar si las DLLs de C++ están presentes
try:
    from pyzbar.pyzbar import decode
    PYZBAR_AVAILABLE = True
except Exception:
    PYZBAR_AVAILABLE = False

def process_evidence_image(image_bytes: bytes) -> dict:
    """
    Analiza capturas de comprobantes o códigos QR de pago.
    Genera un hash SHA-256 para la trazabilidad verificable del caso.
    """
    evidence_hash = hashlib.sha256(image_bytes).hexdigest()
    qr_data = None

    if PYZBAR_AVAILABLE:
        try:
            image = Image.open(io.BytesIO(image_bytes))
            decoded_objects = decode(image)
            if decoded_objects:
                qr_data = decoded_objects[0].data.decode('utf-8')
        except Exception:
            qr_data = None

    return {
        "evidence_hash": evidence_hash,
        "qr_detected_data": qr_data
    }