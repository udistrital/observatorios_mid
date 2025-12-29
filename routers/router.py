from flask import  jsonify, Blueprint, request
from flask_restx import Resource, Api
from controllers import healthCheck, controllerDocumento
from models.model_params import define_parameters
from conf.conf import api_cors_config
from flask_cors import cross_origin, CORS

health_bp = Blueprint('health_bp', __name__)
CORS(health_bp)

@health_bp.route('/', methods=['GET'])
def health():
    return healthCheck.health_check()

# =========================
# API /v1
# =========================

docControl=Blueprint('docControl', __name__)
CORS(docControl)

docDocumentacion = Api(docControl, version='1.0',title="observatorios_mid", description='API para la gestión de lógica de observatorios',doc='/swagger')
docObservatorioscontroller = docDocumentacion.namespace("observatorios_mid",path="/", description="metodos para los procesos de observatorios")
model_params=define_parameters(docDocumentacion)

@docObservatorioscontroller.route('/documento')
class docFirmaElectronica(Resource):
    @docDocumentacion.doc(responses={
        200: 'Success',
        500: 'Nuxeo Error',
        400: 'Bad request'
    }, body=model_params['upload_model'])
    @docObservatorioscontroller.expect(model_params['request_parser'])
    @cross_origin(**api_cors_config)
    def post(self):
        """
            Permite subir un documento a nuxeo consumiendo a gestor documental

            Parameters
            ----------
            request : json
                Json Body {Document}, Documento que será subido

            Returns
            -------
            Response
                Respuesta con cuerpo, status y en formato json
        """
        body=request.get_json()
        return controllerDocumento.postCargarDocumento(body)

    @docDocumentacion.doc(
        responses={200: 'Success', 400: 'Bad request', 500: 'Error interno'},
        body=model_params['update_document_model']
    )
    @cross_origin(**api_cors_config)
    def put(self):
        """
        Actualiza datos de un documento, reemplazando el archivo si ArchivoNuevo = true.
        """
        body = request.get_json()
        return controllerDocumento.putActualizarDocumento(body)

def addRutas(app_main):
    app_main.register_blueprint(health_bp)
    app_main.register_blueprint(docControl, url_prefix='/v1')
