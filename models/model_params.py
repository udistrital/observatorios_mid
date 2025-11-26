from flask_restx import reqparse, fields

def define_parameters(api):

    request_parser = reqparse.RequestParser(bundle_errors=True)
    request_parser.add_argument('list', location='json', type=list, required=True)
    
    return {k: v for k, v in vars().items() if not k.startswith('__')}