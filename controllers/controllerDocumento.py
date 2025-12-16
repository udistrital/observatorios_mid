import logging, json
from flask import Response
from services.gestor_documental_service import GestorDocumentalService
from services.verificacion_virus_service import verificar_virus
from services.observatorios_service import ObservatoriosService
from utils.validador import validar_documento
from utils.response import ApiResponse

def postCargarDocumento(data):
    try:
        if not isinstance(data, list) or len(data) == 0:
            return ApiResponse.error("El body debe ser una lista con al menos un documento").to_flask()
        doc = validar_documento(data[0]["Archivo"])
        id_estructura_archi = data[0]["IdEstructuraArchivosDatos"]
        datos_archivo = data[0]["DatosArchivo"]
        pdf_base64 = doc.get("file")
        if not pdf_base64:
            return ApiResponse.error("El archivo base64 es obligatorio").to_flask()
        virus_result = verificar_virus(pdf_base64)
        if not virus_result.success:
            return ApiResponse.error(virus_result.error, virus_result.status_code).to_flask()
        if virus_result.data["Virus"]["archive"] == "infected":
            #logging.error("El archivo tiene firma de virus y no puede ser procesado.")
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
            return ApiResponse.error("Respuesta inválida del Gestor Documental", 500).to_flask()

        status_gd = response.get("Status")
        if str(status_gd) != "200":
            mensaje = response.get("message") or response.get("error") or "Error en Gestor Documental"
            return ApiResponse.error(mensaje, 500).to_flask()

        enlace = response["res"]["Enlace"]

        datos = datos_archivo
        for key in datos:
            if "hash" in key.lower():
                datos[key] = enlace   

        respuesta_datos = ObservatoriosService.guardar_datos_estructura(
            id_estructura_archi,
            datos
        )

        return ApiResponse.success(respuesta_datos).to_flask()

    except Exception as e:
        return ApiResponse.error(str(e), 500).to_flask()

def putActualizarDocumento(data):
    try:
        if not isinstance(data, list) or len(data) == 0:
            return ApiResponse.error("El body debe ser una lista con un elemento").to_flask()

        payload = data[0]

        id_archivos = payload.get("IdEstructuraArchivosDatos")
        id_documento = payload.get("IdDocumento")
        archivo_nuevo_flag = payload.get("ArchivoNuevo", False)
        datos_archivo = payload.get("DatosArchivo", {})

        if not id_archivos or not id_documento:
            return ApiResponse.error("Faltan IdEstructuraArchivosDatos o IdDocumento").to_flask()

        # 🟦 CASO 1 → NO hay archivo nuevo
        if not archivo_nuevo_flag:
            respuesta_datos = ObservatoriosService.actualizar_datos_estructura(
                id_archivos=id_archivos,
                id_documento=id_documento,
                datos=datos_archivo
            )
            return ApiResponse.success(respuesta_datos).to_flask()

        # 🟦 CASO 2 → Hay archivo nuevo, procesarlo
        archivo = payload.get("Archivo")
        if not archivo:
            return ApiResponse.error(
                "Se indicó ArchivoNuevo=true pero no viene el objeto Archivo"
            ).to_flask()

        doc = validar_documento(archivo)

        pdf_base64 = doc.get("file")
        if not pdf_base64:
            return ApiResponse.error("El archivo base64 es obligatorio").to_flask()

        virus_result = verificar_virus(pdf_base64)
        if not virus_result.success:
            return ApiResponse.error(virus_result.error, virus_result.status_code).to_flask()

        if virus_result.data["Virus"]["archive"] == "infected":
            return ApiResponse.error("El archivo tiene firma de virus y no puede ser procesado.").to_flask()

        payload_gd = [{
            "IdTipoDocumento": doc["IdTipoDocumento"],
            "nombre": doc["nombre"],
            "metadatos": doc.get("metadatos", {}),
            "descripcion": doc.get("descripcion", ""),
            "file": doc["file"]
        }]

        response_gd = GestorDocumentalService.upload_document(payload_gd)

        if not isinstance(response_gd, dict) or str(response_gd.get("Status")) != "200":
            return ApiResponse.error("Error subiendo archivo a Gestor Documental").to_flask()

        enlace = response_gd["res"]["Enlace"]

        for key in datos_archivo:
            if "hash" in key.lower():
                datos_archivo[key] = enlace

        respuesta_datos = ObservatoriosService.actualizar_datos_estructura(
            id_archivos=id_archivos,
            id_documento=id_documento,
            datos=datos_archivo
        )

        return ApiResponse.success(respuesta_datos).to_flask()

    except Exception as e:
        return ApiResponse.error(str(e), 500).to_flask()