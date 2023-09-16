from mysql.connector import Error as mysqlErrors
from flask import request

from models.entidades.canal import Canal
from models.entidades.servidor import Servidor

from models.exceptions import BadRequest
from models.exceptions import DataBaseError
from models.exceptions import CanalNoEncontrado
from models.exceptions import ServidorNoEncontrado

import re

class ControladorCanal:
    @classmethod
    def create_actor(cls):
        datos = request.json

        cls.control_errores(datos)
        
        #creacion de un Canal
        canal = Canal(nombre = datos.get("nombre",""),
                      descripcion = datos.get("descripcion",""),
                      id_servidor = datos.get("id_servidor","")
                      )
        try:
            Canal.crear_canal(canal)
        except mysqlErrors as error:
            raise DataBaseError(f"Se produjo un error al intentar insertar un nuevo canal en la base de datos {error}")
        return {"Mensaje":"Se Creo el canal con exito."}, 201
    
    @classmethod
    def get_canal(cls, id_canal):
        cls.control_error_canal_existe(id_canal)
        try:
            respuesta = Canal.get_canal(id_canal)
        except mysqlErrors as error:
            raise DataBaseError(f"Se prodojo un error en la base de datos al intentar cargar los datos del canal, con id:{id_canal}. {error}")
        return respuesta, 200

    @classmethod
    def get_mensajes(cls, id_canal):
        cls.control_error_canal_existe(id_canal)
        try:
            respuesta = Canal.get_mensajes(id_canal)
        except mysqlErrors as error:
            raise DataBaseError("Se produjo un error al cargar los mensajes del canal con id:{} de la base de datos. {}".format(id_canal,error))
        return respuesta, 200

    @classmethod
    def editar_canal(cls):
        datos = request.json

        cls.control_errores(datos)

        #control de errores id_canal
        if datos.get("id_canal") not in datos:
            raise BadRequest("El id_canal es obligatorio.")
        cls.control_error_canal_existe(datos.get("id_canal"))

        nuevo = Canal(nombre = datos.get("nombre"),
                      descripcion = datos.get("descripcion"),
                      id_servidor = datos.get("id_servidor"),
                      id_canal = datos.get("id_canal")
                      )
        try:
            Canal.editar_canal(canal=nuevo)
        except mysqlErrors as error:
            raise DataBaseError("Se produjo un error al momento de editar el canal con id:{} en la base de datos.{}".format(nuevo.id_canal, error))
        return {"mensaje":"Se modifico con exito el canal con id:{}.".format(nuevo.id_canal)}, 200

    @classmethod
    def eliminar_canal(cls, id_canal):
        cls.control_error_canal_existe(id_canal)
        try:
            Canal.eliminar_canal(id_canal)
        except mysqlErrors as error:
            raise DataBaseError("Se produjo un error al intentar eliminar el canal con id:{} de la base de datos. {}".format(id_canal, error))
        return {"mensaje":"Se elimino con exito el canal con id:{}".format(id_canal)}, 202
    
    @classmethod
    def control_errores(cls, datos):
        #control de errores nombre:
        if "nombre" not in datos:
            raise BadRequest("El nombre del canal es obligatorio.")
        if len(datos["nombre"]) < 2:
            raise BadRequest("El nombre del canal tiene que tener almenos 2 caracteres.")
        if len(datos["nombre"]) > 20:
            raise BadRequest("El nombre del canal tiene que tener 20 o menos caracteres.")
        patron = r"^[a-zA-Z0-9]+$"
        if not (bool(re.match(patron, datos["nombre"]))):
            raise BadRequest("El nombre del canal solo debe tener letra y/o numeros.")
        
        #control de errores descripcion:
        if "descripcion" not in datos:
            raise BadRequest("La descripcion del canal es obligatoria.")
        if len(datos["descripcion"]) < 2:
            raise BadRequest("La descripcion del canal tiene que tener almenos 2 caracteres.")
        if len(datos["descripcion"]) > 45:
            raise BadRequest("La descripcion del canal tiene que tener 45 o menos caracteres.")
        
        #control de errores id_servidor:
        if "id_servidor" not in datos:
            raise BadRequest("No se puede crear el canal sin un id_servidor asociado.")
        try:
            if not (Servidor.existe_servidor(datos.get("id_servidor"))):
                raise ServidorNoEncontrado("No exite un servidor con id={} en la base de datos.".format(datos.get("id_servidor")))
        except mysqlErrors as error:
            raise DataBaseError("Se produjo un error al buscar el servidor ({}) en la base de datos. {}".format(datos.get("id_servidor"), error))
    
    @classmethod
    def control_error_canal_existe(cls, id_canal):
        if id_canal != None:
            try:
                if Canal.existe_canal(id_canal):
                    raise CanalNoEncontrado("El id_canal ({}) no se encuentra en la base de datos.".format(id_canal))
            except mysqlErrors as error:
                raise DataBaseError("Se produjo un error al buscar el canal ({}) en la base de datos. {}".format(id_canal, error))
        else:
            raise BadRequest("El id_canal es obligatorio para completar la solicitud.")