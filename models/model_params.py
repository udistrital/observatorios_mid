from flask_restx import reqparse, fields

def define_parameters(api):

    request_parser = reqparse.RequestParser(bundle_errors=True)
    request_parser.add_argument('list', location='json', type=list, required=True)

    metadata_doc_crud_model = api.model('documentos_crud_metadata', {
        'dato_a': fields.String,
        'dato_b': fields.String,
        'dato_n': fields.String
    })

    upload_model = [api.model('upload_resquest', {
        'IdTipoDocumento': fields.Integer,
        'nombre': fields.String,
        'metadatos': fields.Nested(metadata_doc_crud_model),
        'descripcion': fields.String,
        'file': fields.String
    })]

    archivo_model_put = api.model('archivo_put', {
        'IdTipoDocumento': fields.Integer,
        'nombre': fields.String,
        'metadatos': fields.Raw,
        'descripcion': fields.String,
        'file': fields.String
    })

    update_document_model = api.model('update_document_request', {
        'Archivo': fields.Nested(archivo_model_put, required=False),
        'IdEstructuraArchivosDatos': fields.String(required=True),
        'IdDocumento': fields.String(required=True),
        'ArchivoNuevo': fields.Boolean(required=True),
        'DatosArchivo': fields.Raw(required=True)
    })

    return {k: v for k, v in vars().items() if not k.startswith('__')}