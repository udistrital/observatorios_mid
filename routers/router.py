from flask import  jsonify, Blueprint, request
from flask_restx import Resource, Api
from controllers import healthCheck
from models.model_params import define_parameters
from conf.conf import api_cors_config
from flask_cors import cross_origin, CORS

def addRutas(app_main):
    app_main.register_blueprint(healthCheckController)
    app_main.register_blueprint(docControl, url_prefix='/v1')

healthCheckController = Blueprint('healthCheckController', __name__, url_prefix='/')
CORS(healthCheckController)

@healthCheckController.route('/')
def _():
    return healthCheck.healthCheck(docDocumentacion)

docControl=Blueprint('docControl', __name__)
CORS(docControl)
#----------INICIO SWAGGER --------------
docDocumentacion = Api(docControl, version='1.0',title="observatorios_mid", description='API para la gestión de lógica de observatorios',doc='/swagger')
docFirmacontroller = docDocumentacion.namespace("observatorios_mid",path="/", description="metodos para los procesos de observatorios")

model_params=define_parameters(docDocumentacion)
#----------FIN SWAGGER ----------------
