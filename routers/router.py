from flask import Blueprint, request
from flask_restx import Api, Resource
from flask_cors import CORS, cross_origin
from controllers import controllerDocumento, healthCheck
from models.model_params import define_parameters
from conf.conf import api_cors_config

api_bp = Blueprint("api_bp", __name__)
CORS(api_bp)

docDocumentacion = Api(
    api_bp,
    version="1.0",
    title="observatorios_mid",
    description="API Observatorios MID",
    doc="/swagger"
)

ns_v1 = docDocumentacion.namespace(
    "v1",
    path="/api",
    description="Servicios Observatorios"
)

model_params = define_parameters(docDocumentacion)

@ns_v1.route("/")
class HealthCheck(Resource):

    @cross_origin(**api_cors_config)
    def get(self):
        return healthCheck.health_check()

@ns_v1.route("/v1/documento")
class DocumentoResource(Resource):

    @ns_v1.expect(model_params["request_parser"])
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

    @cross_origin(**api_cors_config)
    def put(self):
        """
        Actualiza datos de un documento, reemplazando el archivo si ArchivoNuevo = true.
        """
        body = request.get_json()
        return controllerDocumento.putActualizarDocumento(body)

def addRutas(app):
    app.register_blueprint(api_bp)
