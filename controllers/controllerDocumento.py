import logging, json
from flask import Response
from services.gestor_documental_service import GestorDocumentalService
from services.verificacion_virus_service import verificar_virus
from utils.validador import validar_documento
from utils.response import ApiResponse

def postCargarDocumento(data):

    try:
        if not isinstance(data, list) or len(data) == 0:
            return ApiResponse.error("El body debe ser una lista con al menos un documento").to_flask()

        doc = validar_documento(data[0])

        pdf_base64 = doc.get("file")
        if not pdf_base64:
            return ApiResponse.error("El archivo base64 es obligatorio").to_flask()

        virus_result = verificar_virus(pdf_base64)
        if not virus_result.success:
            logging.error(f"⚠ Antivirus rechazó el archivo: {virus_result.error}")
            return ApiResponse.error(virus_result.error, virus_result.status_code).to_flask()

        if virus_result.data["Virus"]["archive"] == "infected":
            logging.error("El archivo tiene firma de virus y no puede ser procesado.")
            return ApiResponse.error("El archivo tiene firma de virus y no puede ser procesado.",virus_result.status_code).to_flask()

        payload = [{
            "IdTipoDocumento": doc["IdTipoDocumento"],
            "nombre": doc["nombre"],
            "metadatos": doc.get("metadatos", {}),
            "descripcion": doc["descripcion"],
            "file": doc["file"]
        }]

        response = GestorDocumentalService.upload_document(payload)

        if not isinstance(response, dict):
            logging.error(f"⚠ Respuesta inválida del Gestor Documental: {response}")
            return ApiResponse.error("Respuesta inválida del Gestor Documental", 500).to_flask()

        if str(response.get("Status")) != "200":
            mensaje = response.get("message") or response.get("error") or "Error en Gestor Documental"
            logging.error(f"⚠ Error en Gestor Documental: {mensaje}")
            return ApiResponse.error(mensaje, 500).to_flask()

        return ApiResponse.success(response).to_flask()

    except Exception as e:
        logging.error(f"❌ Error en postCargarDocumento: {str(e)}")
        return ApiResponse.error(str(e), 500).to_flask()