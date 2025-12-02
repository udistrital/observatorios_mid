import logging, json
from flask import Response
from services.gestor_documental_service import GestorDocumentalService
from utils.validador import validar_documento

def postCargarDocumento(data):

    try:
        if not isinstance(data, list) or len(data) == 0:
            raise Exception("El body debe ser una lista con al menos un documento")

        doc = validar_documento(data[0])

        payload = [{
            "IdTipoDocumento": doc["IdTipoDocumento"],
            "nombre": doc["nombre"],
            "metadatos": doc.get("metadatos", {}),
            "descripcion": doc["descripcion"],
            "file": doc["file"]
        }]

        response = GestorDocumentalService.upload_document(payload)

        return Response(json.dumps(response), status=200, mimetype='application/json')

    except Exception as e:
        logging.error(f"❌ Error en postCargarDocumento: {str(e)}")
        error_response = {"error": str(e)}
        return Response(json.dumps(error_response), status=400, mimetype='application/json')