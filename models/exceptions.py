from werkzeug.exceptions import HTTPException
from werkzeug import exceptions
from flask import jsonify

from models.entidades.canal import Canal
from models.entidades.usuario import Usuario
from models.entidades.mensaje import Mensaje
from models.entidades.servidor import Servidor

class BadRequest(exceptions.BadRequest):
    def __init__(self, description = "Solicitud incorrecta"):
        self.description = description
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

class DataBaseError(exceptions.BadHost):
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

class CanalNoEncontrado(exceptions.NotFound):
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
    
    @classmethod
    def existe_canal(cls, id_canal):
        return Canal.existe_canal(id_canal)

class ServidorNoEncontrado(exceptions.NotFound):
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
    @classmethod
    def existe_servidor(cls, id_servidor):
        return Servidor.existe_servidor(id_servidor)

class UsuarioNoEncontrado(exceptions.NotFound):
    def __init__(self, description="No se encontro el usuario en la base de datos."):
        super().__init__(description)
        self.status_code = 500

    def get_response(self):
        response = jsonify({
            "error":{
                "name": "UsuarioNoEncontrado",
                "code":self.code,
                "description":self.description
            }
        })
        response.status_code = self.status_code
        return response
    
    @classmethod
    def existe_usuario(cls, id_usuario):
        return Usuario.existe_usuario(id_usuario)

class MensajeNoEncontrado(exceptions.NotFound):
    def __init__(self, description = "No se encontro el mensaje en la base de datos."):
        super().__init__(description)
        self.status_code = 500

    def get_response(self):
        response = jsonify({
            "error":{
                "name":"MensajeNoEncontrado",
                "code":self.code,
                "description":self.description
            }
        })
        response.status_code = self.status_code
        return response
    
    @classmethod
    def existe_mensaje(cls, id_mensaje):
        return Mensaje.existe_mensaje(id_mensaje)