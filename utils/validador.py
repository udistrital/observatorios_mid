def validar_documento(doc: dict):
    required = ["IdTipoDocumento", "nombre", "descripcion", "file"]

    for field in required:
        if field not in doc:
            raise Exception(f"Falta el campo obligatorio: {field}")

    metadatos = doc.get("metadatos", {})
    if not isinstance(metadatos, dict):
        raise Exception("El campo 'metadatos' debe ser un diccionario")

    file_content = doc.get("file")
    if not isinstance(file_content, str) or not file_content.strip():
        raise Exception("El campo 'file' debe ser un string base64 no vacío")

    return doc
