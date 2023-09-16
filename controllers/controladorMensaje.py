from mysql.connector import Error as mysqlErrors
from flask import request

from models.entidades.mensaje import Mensaje

from models.exceptions import DataBaseError
from models.exceptions import MensajeNoEncontrado
from models.exceptions import UsuarioNoEncontrado
from models.exceptions import CanalNoEncontrado
from models.exceptions import BadRequest

class ControladorMensaje:
    @classmethod    
    def crear_mensaje(cls):
        datos = request.json
        #control errores mensaje
        if "mensaje" not in datos:
            raise BadRequest("El campo mensaje es obligatorio.")
        if datos.get("mensaje") == "":
            raise BadRequest("El mensaje no puede estar vacio.")
        if datos.get("mensaje")>200:
            raise BadRequest("El mensaje no puede tener mas de 200 caracteres.")
        msj = Mensaje(mensaje = datos.get("mensaje", ""),
                      id_canal = datos.get("id_canal", ""),
                      id_usuario = datos.get("id_usuario", ""),
                      id_mensaje_relacionado = datos.get("id_msj_r", "")
                      )
        try:
            Mensaje.crear_mensaje(msj)
        except mysqlErrors as error:
             raise DataBaseError(f"Se produjo un error al intentar insertar un nuevo mensaje en la base de datos {error}")
        return {"Mensaje":"Se Creo el mensaje con exito."}, 201

    @classmethod
    def get_mensaje(cls, id_mensaje):
        try:
            respuesta = Mensaje.get_mensaje(id_mensaje)
        except mysqlErrors as error:
            return {"error":f"Se prodojo un error en la base de datos al intentar cargar los datos del mensaje, con id:{id_mensaje}. {error}"}, 500
        return respuesta, 200
        
    #metodo si se agrega la funcion de editar mensaje
    @classmethod
    def get_mensajes_viejos(cls, id_mensaje):
        try:
            respuesta = Mensaje.get_mensajes_viejos(id_mensaje)
        except mysqlErrors as error:
            return {"error": "Se produjo un error al cargar los mensajes viejos asociados al mensaje con id:{} de la base de datos. {}".format(id_mensaje,error)}, 500
        return respuesta, 200

    @classmethod
    def editar_mensaje(cls):
        datos = request.json
        nuevo = Mensaje(mensaje = datos.get("mensaje",""),
                      id_mensaje = datos.get("id_mensaje")
                      )
        try:
            Mensaje.editar_mensaje(nuevo)
        except mysqlErrors as error:
            return {"error":"Se produjo un error al momento de editar el mensaje con id:{} en la base de datos.{}".format(nuevo.id_mensaje, error)}, 500
        return {"mensaje":"Se modifico con exito el mensaje con id:{}.".format(nuevo.id_mensaje)}, 200