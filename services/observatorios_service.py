import requests
import logging
import os

class ObservatoriosService:

    OBSERVATORIOS_CRUD_URL = os.environ.get("OBSERVATORIOS_CRUD")

    @staticmethod
    def guardar_datos_estructura(id_estructura: str, datos: dict):
        """
        Envía al CRUD los datos asociados al archivo ya registrado en Gestor Documental.
        
        datos → {
            "nombre archivo 1": "22",
            "hash 2": "UUID-del-Gestor-Documental",
            "año": "33"
        }
        """

        if not ObservatoriosService.OBSERVATORIOS_CRUD_URL:
            raise Exception("No está configurada la variable OBSERVATORIOS_CRUD")

        endpoint = f"{ObservatoriosService.OBSERVATORIOS_CRUD_URL}campos/archivos/{id_estructura}/"

        try:
            response = requests.post(endpoint, json=datos, timeout=10)
            logging.info(f"Respuesta al enviar datos de archivo a Observatorios CRUD: {response.status_code} - {response.text}")
            try:
                return response.json()
            except Exception:
                return {
                    "status_code": response.status_code,
                    "raw_response": response.text
                }

        except requests.exceptions.Timeout:
            raise Exception("Timeout al comunicarse con Observatorios CRUD")

        except requests.exceptions.ConnectionError:
            raise Exception(f"No se pudo conectar al CRUD en {endpoint}")

        except Exception as e:
            raise Exception(f"Error inesperado al enviar datos de archivo: {str(e)}")


    @staticmethod
    def actualizar_datos_estructura(id_archivos: str, id_documento: str, datos: dict):
        """
        Actualiza un registro específico dentro del índice de archivos.

        PUT datosArchivo/<id_archivos>/<pk>/
        """

        if not ObservatoriosService.OBSERVATORIOS_CRUD_URL:
            raise Exception("No está configurada la variable OBSERVATORIOS_CRUD")

        # Construir la URL EXACTA del endpoint de actualización
        endpoint = f"{ObservatoriosService.OBSERVATORIOS_CRUD_URL}datosArchivo/{id_archivos}/{id_documento}/"

        try:
            response = requests.put(endpoint, json=datos, timeout=10)

            logging.info(
                f"[PUT] Enviar actualización a Observatorios CRUD "
                f"{response.status_code} - {response.text}"
            )

            try:
                return response.json()
            except Exception:
                return {
                    "status_code": response.status_code,
                    "raw_response": response.text
                }

        except requests.exceptions.Timeout:
            raise Exception("Timeout al comunicarse con Observatorios CRUD")

        except requests.exceptions.ConnectionError:
            raise Exception(f"No se pudo conectar al CRUD en {endpoint}")

        except Exception as e:
            raise Exception(f"Error inesperado al actualizar datos de archivo: {str(e)}")

