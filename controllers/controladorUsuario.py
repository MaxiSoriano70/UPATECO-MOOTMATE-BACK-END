from mysql.connector import Error as mysqlErrors
from flask import request

from models.entidades.usuario import Usuario

class ControladorUsuario:
    @classmethod
    def crear_usuario(cls):
        datos = request.json
        usuario = Usuario(nombre = datos.get("nombre", ""),
                          apellido = datos.get("apellido", ""),
                          correo = datos.get("correo", ""),
                          password = datos.get("password","")
                          )
        try:
            Usuario.crear_usuario(usuario)
        except mysqlErrors as error:
            return {"error": f"Se produjo un error al intentar insertar un nuevo usuario en la base de datos {error}"}, 500
        return {"Mensaje":"Se Creo el usuario con exito."}, 201
    
    @classmethod
    def get_usuario(cls, id_usuario:int):
        try:
            respuesta = Usuario.get_usuario(id_usuario)
        except mysqlErrors as error:
            return {"error":f"Se prodojo un error en la base de datos al intentar cargar los datos del usuario, con id:{id_usuario}. {error}"}, 500
        return respuesta, 200
    
    @classmethod
    def get_servidores(cls, id_usuario:int):
        try:
            respuesta = Usuario.get_servidores(id_usuario)
        except mysqlErrors as error:
            return {"error": "Se produjo un error al cargar los servidores del usuario con id={} de la base de datos. {}".format(id_usuario,error)}, 500
        return respuesta, 200

    @classmethod
    def get_privilegio(cls, id_usuario, id_servidor):
        try:
            respuesta = Usuario.get_privilegio(id_usuario, id_servidor)
        except mysqlErrors as error:
            return {"error": "Se produjo un error al cargar los privilegios del usuario con id={} en el servidor con id={} de la base de datos. {}".format(id_usuario, id_servidor, error)}, 500
        return respuesta, 200

    @classmethod
    def get_usuarios(cls):
        try:
            respuesta = Usuario.get_usuarios()
        except mysqlErrors as error:
            return {"error": "Se produjo un error al cargar todos los usuarios de la base de datos. {}".format(error)}, 500
        return respuesta, 200
    
    @classmethod
    def actualizar_usuario(cls):
        datos = request.json
        nuevo = Usuario(nombre = datos.get("nombre", ""),
                          apellido = datos.get("apellido", ""),
                          alias = datos.get("alias", ""),
                          correo = datos.get("correo", ""),
                          password = datos.get("password", ""),
                          tipo_estado = datos.get("estado", ""),
                          codigo_verificacion = datos.get("cod_ver", ""),
                          id_usuario = datos.get("id_usuario", "")
                          )
        try:
            Usuario.actualizar_usuario(nuevo)
        except mysqlErrors as error:
            return {"error":"Se produjo un error al momento de actualizar los datos del usuario con id={} en la base de datos.{}".format(nuevo.id_usuario, error)}, 500
        return {"mensaje":"Se modifico con exito los datos del usuario con id={}.".format(nuevo.id_usuario)}, 200

    @classmethod
    def eliminar_usuario(cls, id_usuario: int):
        try:
            Usuario.eliminar_usuario(id_usuario)
        except mysqlErrors as error:
            return {"error":"Se produjo un error al intentar eliminar el usuario con id={} de la base de datos. {}".format(id_usuario, error)}, 500
        return {"mensaje":"Se elimino con exito el usuario con id={}".format(id_usuario)}, 202
        
    @classmethod
    def agregar_servidor(cls, id_usuario, id_servidor):
        try:
            Usuario.agregar_servidor(id_usuario,id_servidor)
        except mysqlErrors as error:
            return {"error":"Se produjo un error en la base de datos, al intentar unir al usuario con id={} al servidor con id={}. {}".format(id_usuario, id_servidor, error)}
        return {"mensaje":"Se agrego con exito al usuario con id={} al servidor con id={}.".format(id_usuario,id_servidor)}