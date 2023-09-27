from models.baseDeDatos import BaseDeDatos

import hashlib  

class Usuario:
    def __init__(self, nombre:str, apellido:str, alias:str, correo:str,
                 password:str, estado = 'conectado', codigo_verificacion:str = None, id_usuario:int = None):
        self.nombre = nombre
        self.apellido = apellido
        self.alias = alias
        self.correo = correo
        self.password = password
        self.estado = estado
        self.codigo_verificacion = codigo_verificacion
        self.id_usuario = id_usuario
    
    @classmethod
    def crear_usuario(cls, usuario):
        consulta = """INSERT INTO mootmate.usuarios
        (nombre, apellido, alias, correo, password, estado, codigo_verificacion)
        values (%s,%s,%s,%s,%s,%s,%s)"""

        parametros = (  usuario.nombre,
                        usuario.apellido,
                        usuario.alias,
                        usuario.correo,
                        usuario.password,
                        usuario.estado,
                        usuario.codigo_verificacion)
        BaseDeDatos.ejecutar_consulta(consulta, parametros)
    
    @classmethod
    def verificar_usuario(cls, id_usuario):
        consulta = """UPDATE mootmate.usuarios as u SET u.verificado = 1, u.codigo_verificacion = NULL WHERE u.id_usuario = %s"""
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=id_usuario)
    
    @classmethod
    def get_cod_verificacion(cls, id_usuario):
        consulta = """SELECT u.codigo_verificacion FROM mootmate.usuarios as u
        WHERE u.id_usuario = %s"""
        respuesta = BaseDeDatos.traer_uno(consulta=consulta, parametros=id_usuario)
        return respuesta[0]

    @classmethod
    def get_usuario(cls, id_usuario:int):
        consulta = """SELECT * FROM mootmate.usuarios as u
        WHERE u.id_usuario = %s"""
        response = BaseDeDatos.traer_uno(consulta=consulta, parametros=id_usuario, diccionario=True)
        return response
    
    @classmethod
    def get_servidores(cls, id_usuario:int):
        consulta = """SELECT s.id_servidor, s.nombre, s.descripcion, s.fecha_creacion
        FROM usuarios as u INNER JOIN usuarios_servidores as u_s ON u.id_usuario = u_s.id_usuario
        INNER JOIN servidores as s ON u_s.id_servidor = s.id_servidor
        WHERE u.id_usuario = %s"""
        datos = BaseDeDatos.traer_todo(consulta=consulta, parametros=id_usuario, diccionario=True)
        respuesta = {"servidores":datos}
        return respuesta

    @classmethod
    def get_privilegio(cls, id_usuario, id_servidor):
        consulta = """SELECT u_s.privilegio_usuario FROM mootmate.usuarios_servidores as u_s
        WHERE u_s.id_usuario = %s AND u_s.id_servidor = %s"""
        respuesta = BaseDeDatos.traer_uno(consulta=consulta, parametros=(id_usuario,id_servidor), diccionario=True)
        return respuesta

    @classmethod
    def get_usuarios(cls):
        consulta = """SELECT * FROM mootmate.usuarios"""
        respuesta = BaseDeDatos.traer_todo(consulta=consulta,diccionario=True)
        usuarios = list(respuesta)
        return usuarios
    
    @classmethod
    def actualizar_usuario(cls, usuario):
        consulta = """UPDATE mootmate.usuarios as u SET
        u.nombre = %s,
        u.apellido = %s,
        u.alias = %s,
        u.correo = %s,
        u.password = %s,
        u.estado = %s,
        u.codigo_verificacion = %s
        WHERE u.id_usuario = %s"""
        parametros = (  usuario.nombre,
                        usuario.apellido,
                        usuario.alias,
                        usuario.correo,
                        usuario.password,
                        usuario.estado,
                        usuario.codigo_verificacion,
                        usuario.id_usuario)
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=parametros)
    
    @classmethod
    def cambiar_estado(cls, id_usuario:int, estado:str):
        consulta = """UPDATE mootmate.usuarios as u SET u.estado = %s
        WHERE u.id_usuario = %s"""
        parametros = (estado,id_usuario)
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=parametros)

    @classmethod
    def eliminar_usuario(cls, id_usuario: int):
        cls.cambiar_estado(id_usuario, "eliminado")
        
    @classmethod
    def existe_usuario(cls, id_usuario):
        consulta = """SELECT u.id_usuario FROM mootmate.usuarios as u WHERE u.id_usuario = %s"""
        response = BaseDeDatos.traer_uno(consulta=consulta,parametros=id_usuario)
        return response != None
    
    @classmethod
    def agregar_servidor(cls, id_usuario, id_servidor):
        consulta = """INSERT INTO mootmate.usuarios_servidores (id_servidor, id_usuario, privilegio_usuario)
        Values (%s,%s,%s)"""
        parametros = (id_servidor, id_usuario,"comun")
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=parametros)
    
    @classmethod
    def usuario_eliminado(cls, id_usuario):
        consulta = """SELECT * FROM mootmate.usuarios as u WHERE u.id_usuario = %s AND u.estado='eliminado'"""
        respuesta = BaseDeDatos.traer_uno(consulta=consulta, parametros=id_usuario)
        return respuesta != None
    
    @classmethod
    def create_password(cls, password):
        halg = hashlib.sha256()
        halg.update(password.encode('utf-8'))
        hash_password = halg.hexdigest()
        return hash_password
        
    def serealizar_usuario(self):
        serial = {"nombre": self.nombre,
                  "apellido": self.apellido,
                  "alias": self.alias,
                  "correo": self.correo,
                  "password": self.password,
                  "estatado": self.estado,
                  "codigo_verificacion": self.codigo_verificacion,
                  "id": self.id_usuario}
        return serial
