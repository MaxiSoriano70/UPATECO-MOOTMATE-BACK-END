from werkzeug.exceptions import HTTPException
from flask import jsonify

class BadRequest(HTTPException):
    def __init__(self, description = "Solicitud incorrecta"):
        super().__init__(description)
        self.status_code = 400

    def get_response(self):
        response = jsonify({
            "error":{
                "code":self.code,
                "description":self.description
            }
        })
        response.status_code = self.status_code
        return response

class DataBaseError(HTTPException):
    def __init__(self, description = "Ocurrio un error al intentar procesar la consulta en la base de datos."):
        super().__init__(description)
        self.status_code = 500

    def get_response(self):
        response = jsonify({
            "error":{
                "code":self.code,
                "description":self.description
            }
        })
        response.status_code = self.status_code
        return response

class CanalNoEncontrado(HTTPException):
    def __init__(self, description = "No se encontro el canal en la base de datos."):
        super().__init__(description)
        self.status_code = 500

    def get_response(self):
        response = jsonify({
            "error":{
                "name":"CanalNoEncontrado",
                "code":self.code,
                "description":self.description
            }
        })
        response.status_code = self.status_code
        return response

class ServidorNoEncontrado(HTTPException):
    def __init__(self, description = "No se encontro el servidor en la base de datos."):
        super().__init__(description)
        self.status_code = 500

    def get_response(self):
        response = jsonify({
            "error":{
                "name":"ServidorNoEncontrado",
                "code":self.code,
                "description":self.description
            }
        })
        response.status_code = self.status_code
        return response

class UsuarioNoEncontrado(HTTPException):
    def __init__(self, description = "No se encontro el usuario en la base de datos."):
        super().__init__(description)
        self.status_code = 500

    def get_response(self):
        response = jsonify({
            "error":{
                "name":"UsuarioNoEncontrado",
                "code":self.code,
                "description":self.description
            }
        })
        response.status_code = self.status_code
        return response