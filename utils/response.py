import json
from flask import Response

class ApiResponse:
    """
    Genera respuestas uniformes para toda la API.
    """

    def __init__(self, success: bool, status_code: int, data=None, error=None):
        self.success = success
        self.status_code = status_code
        self.data = data
        self.error = error

    def to_dict(self):
        return {
            "success": self.success,
            "statusCode": self.status_code,
            "data": self.data,
            "error": self.error
        }

    def to_flask(self):
        """
        Convierte el objeto ApiResponse en una respuesta Flask estandarizada.
        """
        return Response(
            json.dumps(self.to_dict()),
            status=self.status_code,
            mimetype="application/json"
        )

    @staticmethod
    def success(data=None, status_code=200):
        return ApiResponse(True, status_code, data=data)

    @staticmethod
    def error(message, status_code=400):
        return ApiResponse(False, status_code, error=message)