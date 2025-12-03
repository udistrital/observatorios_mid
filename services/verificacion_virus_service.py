import json
import logging
import os
import requests

class VirusScanResponse:
    """Estructura estándar de respuesta interna del servicio."""

    def __init__(self, success: bool, status_code: int, data=None, error=None):
        self.success = success
        self.status_code = status_code
        self.data = data
        self.error = error

    def to_dict(self):
        """Devuelve la estructura lista para serializar."""
        return {
            "success": self.success,
            "statusCode": self.status_code,
            "data": self.data,
            "error": self.error,
        }

def _safe_json(response):
    """
    Intenta parsear JSON de forma segura.
    Retorna None si no es JSON válido.
    """
    try:
        return response.json()
    except Exception:
        logging.error("Respuesta no es JSON válido: %s", response.text)
        return None

def verificar_virus(pdf_base64: str) -> VirusScanResponse:
    """
    Envía un PDF (en base64) al antivirus y retorna el estado "clean" o "infected".
    """
    if not pdf_base64 or not isinstance(pdf_base64, str):
        return VirusScanResponse(
            success=False,
            status_code=400,
            error="El contenido PDF base64 no es válido o está vacío."
        )

    payload = {"pdf_base64": pdf_base64}
    endpoint = os.environ.get("ESCANEAR_ARCHIVO") + "/verificar"
    response = requests.post(endpoint, json=payload, timeout=16)
    lambda_outer = _safe_json(response)

    if lambda_outer is None:
        return VirusScanResponse(False, 500, error="Respuesta inválida del antivirus (no JSON).")

    try:
        lambda_inner = json.loads(lambda_outer.get("body", "{}"))
    except Exception:
        return VirusScanResponse(False, 500, error="No se pudo decodificar el JSON interno del antivirus.")

    if lambda_inner.get("status") not in ("clean", "infected"):
        return VirusScanResponse(False, 500, error="Respuesta inválida recibida desde el antivirus.")

    return VirusScanResponse(
        success=True,
        status_code=200,
        data={
            "Virus": {
                "message": "La verificación se completó correctamente.",
                "archive": lambda_inner.get("status"),
                "raw_output": lambda_inner.get("raw_output", ""),
                "statusCode": lambda_outer.get("statusCode", 200)
            }
        }
    )
