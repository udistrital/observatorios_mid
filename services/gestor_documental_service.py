import os
import requests
import logging

class GestorDocumentalService:

    BASE_URL = os.environ.get("GESTOR_DOCUMENTAL_URL")

    @staticmethod
    def upload_document(payload: list):
        """Envía documento al gestor documental."""

        if not GestorDocumentalService.BASE_URL:
            raise Exception("No está configurada la variable GESTOR_DOCUMENTAL_URL")

        endpoint = GestorDocumentalService.BASE_URL + "document/uploadAnyFormat"

        try:
            response = requests.post(endpoint, json=payload, timeout=12)

            try:
                return response.json()
            except Exception:
                return {
                    "status_code": response.status_code,
                    "raw_response": response.text
                }

        except requests.exceptions.Timeout:
            raise Exception("Timeout al comunicarse con Gestor Documental")

        except requests.exceptions.ConnectionError:
            raise Exception(f"No se pudo conectar al Gestor Documental en {endpoint}")

        except Exception as e:
            raise Exception(f"Error inesperado al enviar documento: {str(e)}")
