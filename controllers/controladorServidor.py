from mysql.connector import Error as mysqlErrors
from flask import request

from models.entidades.servidor import Servidor

class ControladorServidor:
    @classmethod
    def crear_servidor(cls):
        datos = request.json
        servidor = Servidor(nombre = datos.get("nombre", ""),
                            descripcion = datos.get("descripcion", ""),
                            id_usuario_creador = datos.get("id_usuario")
                            )
        try:
            Servidor.crear_servidor(servidor)
        except mysqlErrors as error:
            return {"error": f"Se produjo un error al intentar insertar un nuevo servidor en la base de datos {error}"}, 500
        return {"Mensaje":"Se Creo el servidor con exito."}, 201

    @classmethod
    def get_servidor(cls, id_servidor:int):
        try:
            respuesta = Servidor.get_servidor(id_servidor)
        except mysqlErrors as error:
            return {"error":f"Se prodojo un error en la base de datos al intentar cargar los datos del servidor, con id:{id_servidor}. {error}"}, 500
        return respuesta, 200
        
    @classmethod
    def get_usuario_creador(cls, id_servidor):
        try:
            respuesta = Servidor.get_usuario_creador(id_servidor)
        except mysqlErrors as error:
            return {"error":"Se produjo un error al cargar el usuario que creo el servidor con id={}. {}".format(id_servidor,error)}, 500
        return respuesta, 200

    @classmethod
    def get_usuarios(cls, id_servidor:int):
        try:
            respuesta = Servidor.get_usuarios(id_servidor)
        except mysqlErrors as error:
            return {"error":"Se produjo un error al intentar cargar todos los usuarios del servidor con id={}. {}".format(id_servidor, error)}, 500
        return respuesta, 200

    @classmethod
    def get_canales(cls, id_servidor:int):
        try:
            respuesta = Servidor.get_canales(id_servidor)
        except mysqlErrors as error:
            return {"error":"Se produjo un error al intentar cargar todos los canales del servidor con id={}. {}".format(id_servidor, error)}, 500
        return respuesta, 200
    
    @classmethod
    def editar_servidor(cls):
        datos = request.json
        nuevo = Servidor(nombre = datos.get("nombre", ""),
                         descripcion = datos.get("descripcion", ""),
                         id_servidor = datos.get("id_servidor", "")
                         )
        try:
            Servidor.editar_servidor(nuevo)
        except mysqlErrors as error:
            return {"error":"Se produjo un error al momento de editar el servidor con id:{} en la base de datos.{}".format(nuevo.id_servidor, error)}, 500
        return {"mensaje":"Se modifico con exito el canal con id:{}.".format(nuevo.id_servidor)}, 200

    @classmethod
    def eliminar_servidor(cls, id_servidor:int):
        try:
            Servidor.eliminar_servidor(id_servidor)
        except mysqlErrors as error:
            return {"error":"Se produjo un error al intentar eliminar el servidor con id:{} de la base de datos. {}".format(id_servidor, error)}, 500
        return {"mensaje":"Se elimino con exito el servidor con id:{}".format(id_servidor)}, 202
    
    @classmethod
    def eliminar_usuario(cls, id_servidor:int, id_usuario:int):
        try:
            Servidor.eliminar_usuario(id_servidor,id_usuario)
        except mysqlErrors as error:
            return {"error":"Se produjo un error en la base de datos al intentar eliminar al usuario con id={} del servidor con id={}. {}".format(id_usuario,id_servidor,error)}, 500
        return {"Mensaje":"Se elimino con exito el usuario con id={} del servidor con id={}.".format(id_usuario,id_servidor)}, 202