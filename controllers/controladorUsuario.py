from mysql.connector import Error as mysqlErrors
from flask import request, session, jsonify
from config import Config
import re
import random
import os
from models.entidades.usuario import Usuario
from models.entidades.servidor import Servidor

from models.exceptions import DataBaseError
from models.exceptions import UsuarioNoEncontrado
from models.exceptions import ServidorNoEncontrado
from models.exceptions import BadRequest
#from werkzeug.exceptions import BadRequest

class ControladorUsuario:
    @classmethod
    def crear_usuario(cls):
        datos = request.json
        #control de errores nombre
        if "nombre" not in datos:
            raise BadRequest("El nombre del usuario es obligatorio.")
        if len(datos.get("nombre"))<2:
            raise BadRequest("El nombre de usuario tiene que tener almenos 2 caracteres.")
        if len(datos.get("nombre"))>30:
            raise BadRequest("El nombre del usuario tiene que tener un maximo de 30 caracteres.")
        patron = r"^[A-Za-z]+(?: [A-Za-z]+)*$"
        if not(re.match(patron, datos.get("nombre"))):
            raise BadRequest("El nombre de usuario tiene que tener solo letras.")
        
        #control de errores apellido
        if "apellido" not in datos:
            raise BadRequest("El apellido del usuario es obligatorio.")
        if len(datos.get("apellido"))<2:
            raise BadRequest("El apellido de usuario tiene que tener almenos 2 caracteres.")
        if len(datos.get("apellido"))>30:
            raise BadRequest("El apellido del usuario tiene que tener un maximo de 30 caracteres.")
        if not(re.match(patron, datos.get("apellido"))):
            raise BadRequest("El apellido de usuario tiene que tener solo letras.")
        
        #control de correo
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if "correo" not in datos:
            raise BadRequest("El correo de usuario es obligatorio.")
        if not(re.match(patron, datos.get("correo"))):
            raise BadRequest("El correo {} no es valido".format(datos.get("correo")))
        
        #control contraseña:
        patron = r'^(?=.*[A-Za-z0-9!@#$%^&*()_+])[A-Za-z0-9!@#$%^&*()_+]{8,}$'
        if "password" not in datos:
            raise BadRequest("La cotraseña es obligatoria.")
        if not(re.match(patron, datos.get("password"))):
            raise BadRequest("La contraseña no cumple los requisitos necesarios.")
        
        #control alias
        if "alias" not in datos:
            raise BadRequest("El alias del usuario es obligatorio.")
        if len(datos.get("alias"))<2:
            raise BadRequest("El alias de usuario tiene que tener almenos 2 caracteres.")
        if len(datos.get("nombre"))>30:
            raise BadRequest("El alias del usuario tiene que tener un maximo de 30 caracteres.")
        patron = r"^[a-zA-Z0-9]+$"
        if not(re.match(patron, datos.get("alias"))):
            raise BadRequest("El alias de usuario tiene que tener solo letras.")

        usuario = Usuario(nombre = datos.get("nombre", ""),
                          apellido = datos.get("apellido", ""),
                          correo = datos.get("correo", ""),
                          password = Usuario.create_password(datos.get("password","")),
                          alias=datos.get("alias", ""),
                          codigo_verificacion = cls.crear_token()
                          )
        
        if Usuario.existe_correo(usuario):
            raise BadRequest("El correo ya se encuetra registrado")
        
        if Usuario.existe_alias(usuario):
            raise BadRequest("El ALias ya se encuetra registrado")
        
        try:
            Usuario.crear_usuario(usuario)
        except mysqlErrors as error:
            raise DataBaseError(f"Se produjo un error al intentar insertar un nuevo usuario en la base de datos {error}")
        return {"Mensaje":"Se Creo el usuario con exito."}, 201
    
    @classmethod
    def get_usuario(cls, id_usuario:int):
        cls.control_existe_usuario(id_usuario)

        try:
            respuesta = Usuario.get_usuario(id_usuario)
        except mysqlErrors as error:
            raise DataBaseError(f"Se prodojo un error en la base de datos al intentar cargar los datos del usuario, con id:{id_usuario}. {error}")
        return respuesta, 200
    
    @classmethod
    def get_servidores(cls, id_usuario:int):
        cls.control_existe_usuario(id_usuario)

        try:
            respuesta = Usuario.get_servidores(id_usuario)
        except mysqlErrors as error:
            raise DataBaseError("Se produjo un error al cargar los servidores del usuario con id={} de la base de datos. {}".format(id_usuario,error))
        return respuesta, 200

    @classmethod
    def get_privilegio(cls, id_usuario, id_servidor):
        cls.control_existe_usuario(id_usuario)

        try:
            respuesta = Usuario.get_privilegio(id_usuario, id_servidor)
            ServidorNoEncontrado.existe_servidor(id_servidor)
        except mysqlErrors as error:
            raise DataBaseError("Se produjo un error al cargar los privilegios del usuario con id={} en el servidor con id={} de la base de datos. {}".format(id_usuario, id_servidor, error))
        return respuesta, 200

    @classmethod
    def get_usuarios(cls):
        try:
            respuesta = Usuario.get_usuarios()
        except mysqlErrors as error:
            raise DataBaseError("Se produjo un error al cargar todos los usuarios de la base de datos. {}".format(error))
        return {"usuarios":respuesta}, 200
    
    @classmethod
    def actualizar_usuario(cls):
        datos = request.json
        #control de errores nombre
        if "nombre" in datos:
            patron = r"^[A-Za-z]+(?: [A-Za-z]+)*$"
            if len(datos.get("nombre"))<2:
                raise BadRequest("El nombre de usuario tiene que tener almenos 2 caracteres.")
            if len(datos.get("nombre"))>30:
                raise BadRequest("El nombre del usuario tiene que tener un maximo de 30 caracteres.")
            if not(re.match(patron, datos.get("nombre"))):
                raise BadRequest("El nombre de usuario tiene que tener solo letras.")
        #control de errores apellido
        if "apellido" in datos:
            patron = r"^[a-zA-Z]+$"            
            if len(datos.get("apellido"))<2:
                raise BadRequest("El apellido de usuario tiene que tener almenos 2 caracteres.")
            if len(datos.get("apellido"))>30:
                raise BadRequest("El apellido del usuario tiene que tener un maximo de 30 caracteres.")
            if not(re.match(patron, datos.get("apellido"))):
                raise BadRequest("El apellido de usuario tiene que tener solo letras.")
        
        #control contraseña:
        nuevopassword = ''
        if "password" in datos:
            patron = r'^(?=.*[A-Za-z0-9!@#$%^&*()_+])[A-Za-z0-9!@#$%^&*()_+]{8,}$'
            if not(re.match(patron, datos.get("password"))):
                raise BadRequest("La contraseña no cumple los requisitos necesarios.")
            nuevopassword= datos.get('password')
        if nuevopassword != '':
            nuevopassword = Usuario.create_password(nuevopassword)
        #control alias:
        """if "alias" in datos:
            if datos.get("alias") < 2:
                raise BadRequest("El alias de usuario tiene que tener almenos 2 caracteres.")
            if datos.get("alias") > 30:
                raise BadRequest("El alias del usuario tiene que tener un maximo de 30 caracteres.")"""
        
        #control de estado:
        if "estado" in datos:
            estados = ("conectado", "desconectado", "ausente", "no_molestar", "eliminado")
            if datos.get("estado") not in estados:
                raise BadRequest("Solo se permite uno de los siguientes estados {}".format(estados))
        
        #contro id_usuario:
        if "alias" not in datos:
            raise BadRequest("El alias es obligatorio")
        """else:
            cls.control_existe_usuario(datos.get("id_usuario"))"""
            
        #control de correo
        if "correo" in datos:
            patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not(re.match(patron, datos.get("correo"))):
                raise BadRequest("El correo {} no es valido".format(datos.get("correo")))
            
            nuevo = Usuario(nombre = datos.get("nombre", ""),
                            apellido = datos.get("apellido", ""),
                            alias = datos.get("alias", ""),
                            correo = datos.get("correo", ""),
                            password = nuevopassword,
                            estado = datos.get("estado", "Conectado"),
                            codigo_verificacion = cls.crear_token(),
                            id_usuario = datos.get("id_usuario", "")
                            )
        else:
            nuevo = Usuario(nombre = datos.get("nombre", ""),
                            apellido = datos.get("apellido", ""),
                            alias = datos.get("alias", ""),
                            password = nuevopassword,
                            estado = datos.get("estado", "Conectado"),
                            id_usuario = datos.get("id_usuario", ""),
                            correo = datos.get("correo", "")
                            )
        try:
            
            Usuario.actualizar_usuario(nuevo)
        except mysqlErrors as error:
            raise DataBaseError("Se produjo un error al momento de actualizar los datos del usuario con id={} en la base de datos.{}".format(nuevo.id_usuario, error))
        return {"mensaje":"Se modifico con exito los datos del usuario con alias={}.".format(nuevo.alias)}, 200

    @classmethod
    def eliminar_usuario(cls, id_usuario: int):
        cls.control_existe_usuario(id_usuario)

        if not(Usuario.existe_usuario(id_usuario)):
            raise UsuarioNoEncontrado()
        try:
            Usuario.eliminar_usuario(id_usuario)
        except mysqlErrors as error:
            raise DataBaseError("Se produjo un error al intentar eliminar el usuario con id={} de la base de datos. {}".format(id_usuario, error))
        return {"mensaje":"Se elimino con exito el usuario con id={}".format(id_usuario)}, 202
        
    @classmethod
    def agregar_servidor(cls, id_usuario, id_servidor):
        cls.control_existe_usuario(id_usuario)
        try:
            if not ServidorNoEncontrado.existe_servidor(id_servidor):
                return {"mensaje":"Se agrego con exito al usuario con id={} al servidor con id={}.".format(id_usuario,id_servidor)}
                raise ServidorNoEncontrado("Servidor no encontrado")
            Usuario.agregar_servidor(id_usuario,id_servidor)
        except mysqlErrors as error:
            raise DataBaseError("Se produjo un error en la base de datos, al intentar unir al usuario con id={} al servidor con id={}. {}".format(id_usuario, id_servidor, error))
        return {"mensaje":"Se agrego con exito al usuario con id={} al servidor con id={}.".format(id_usuario,id_servidor)}
    
    @classmethod
    def crear_token(cls):
        lista = ["A"]*6
        for index in range(6):
            num_asicii = random.randint(48,90)
            while num_asicii > 57 and num_asicii < 65:
                num_asicii = random.randint(48,90)
            lista[index] = chr(num_asicii)
        
        token = "".join(lista)
        return token
    
    @classmethod
    def control_existe_usuario(cls, id_usuario):
        try:
            if not(Usuario.existe_usuario(id_usuario)):
                raise UsuarioNoEncontrado(description="El usuario con id={} no se encontro en la base de datos.".format(id_usuario))
        except mysqlErrors as error:
            raise DataBaseError("Se produjo un error al en la base de datos al intetar obtener datos del usuario. {}".format(error))
    
    @classmethod
    def show_profile(cls):
        alias = session.get('alias')
        try:
            respuesta = Usuario.get_profile(alias)
        except mysqlErrors as error:
            raise DataBaseError(f"Se prodojo un error en la base de datos al intentar cargar los datos del usuario, con alias:{alias}. {error}")
        return respuesta, 200
    
    @classmethod
    def logout(cls):
        session.pop('alias', None)
        return {"message": "Sesion cerrada"}, 200
    
    @classmethod
    def actualizar_foto(cls):
        try:
            
            nueva_imagen = request.files['imagen'] if 'imagen' in request.files else None
            id_usuario   = request.form.get('id_usuario')

            if nueva_imagen:
                ruta_imagen = os.path.join(Config.UPLOAD_FOLDER, f"{id_usuario}.jpg")
                nueva_imagen.save(ruta_imagen)
              
                Usuario.actualizar_ruta(id_usuario, ruta_imagen)
                
                return jsonify({"mensage": "Imagen actualizada correctamente"}), 200
            else:
                return jsonify({"mensage": "No se proporcionó una nueva imagen"}), 400
        except Exception as e:
                return jsonify({"mesnage": str(e)}), 500