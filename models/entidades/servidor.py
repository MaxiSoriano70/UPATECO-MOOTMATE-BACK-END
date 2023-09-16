from models.baseDeDatos import BaseDeDatos  
from models.entidades.usuario import Usuario

class Servidor:
    def __init__(self, nombre:str, descripcion:str, id_usuario_creador:int, id_servidor:int = None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.id_usuario_creador = id_usuario_creador
        self.id_servidor = id_servidor

    @classmethod
    def crear_servidor(cls, servidor):
        consulta = """INSERT INTO mootmate.servidores (nombre, descripcion)
        values (%s,%s)"""
        parametros = (servidor.nombre, servidor.descripcion)
        cursor = BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=parametros)
        servidor.id_servidor = cursor.lastrowid
        consulta = """INSERT INTO mootmate.usuarios_servidores
        (id_usuario, id_servidor, id_privilegio_usuario)
        values (%s,%s,%s)"""
        #por defecto diremos que 1 = Admin como ejemplo pero esto se debe definir a la hora
        #de cargar los distintos tipos de privilegios
        parametros = (servidor.id_usuario_creador, servidor.id_servidor, 1)
        BaseDeDatos.ejecutar_consulta(consulta=consulta,parametros=parametros)

    @classmethod
    def get_servidor(cls, id_servidor:int ):
        consulta = """SELECT * FROM mootmate.servidor as u WHERE u.id_servidor = %s"""
        return BaseDeDatos.traer_uno(consulta=consulta, parametros=id_servidor, diccionario=True)
        
    @classmethod
    def get_usuario_creador(cls, id_servidor):
        consulta = """SELECT u_s.id_usuario FROM mootmate.usuarios_servidores as u_s WHERE u_s.id_servidor = %s"""
        respuesta = BaseDeDatos.traer_uno(consulta=consulta, parametros=id_servidor)
        usuario = Usuario.get_usuario(respuesta[0])
        return usuario

    @classmethod
    def get_usuarios(cls, id_servidor:int):
        consulta = """SELECT u_s.id_usuario FROM mootmate.usuarios_servidores as u_s WHERE u_s.id_servidor = %s"""
        respuesta = BaseDeDatos.traer_todo(consulta=consulta, parametros=id_servidor)
        usuarios = []
        for usuario in respuesta:
            usuario = Usuario.get_usuario(usuario[0])
            usuarios.append(usuario)
        return {"usuarios":usuarios}

    @classmethod
    def get_canales(cls, id_servidor:int):
        consulta = """SELECT * FROM mootmate.canales as c WHERE c.id_servidor = %s"""
        respuesta = BaseDeDatos.traer_todo(consulta=consulta, parametros=id_servidor, diccionario=True)
        return {"canales":respuesta}
    
    @classmethod
    def editar_servidor(cls, nuevo):
        consulta = """UPDATE FROM mootmate.servidores as s SET
        s.nombre = %s,
        s.descripcion = %s
        WHERE s.id_servidor = %s"""
        parametros = (nuevo.nombre, nuevo.descripcion, nuevo.id_servidor)
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=parametros)

    @classmethod
    def eliminar_servidor(cls, id_servidor:int):
        consulta = """DELETE FROM mootmate.servidor as s WHERE s.id_servidor = %s"""
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=id_servidor)
        consulta = """DELETE FROM mootmate.usuarios_servidores as u_s WHERE u_s.id_server = %s"""
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=id_servidor)

    @classmethod
    def existe_servidor(cls, id_servidor:int):
        consulta = """SELECT s.id_servidor FROM mootmate.servidores as s WHERE s.id_servidor = %s"""
        respuesta = BaseDeDatos.traer_uno(consulta=consulta, parametros=id_servidor)
        if respuesta != None:
            return True
        else:
            return False
    
    @classmethod
    def existe_usuario_servidor(cls, id_servidor, id_usuario):
        respuesta = False
        usuarios = cls.get_usuarios(id_servidor)
        for usuario in usuarios["usuarios"]:
            if usuario["id_usuario"] == id_usuario:
                respuesta = True
                break
        return respuesta
    
    @classmethod
    def eliminar_usuario(cls, id_servidor, id_usuario):
        consulta = """DELETE FROM mootmate.usuarios_servidores as u_s WHERE u_s.id_servidor = %s AND u_s.id_usuario = %s"""
        parametros = (id_servidor, id_usuario)
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=parametros)
        
    def serealizar_servidor(self):
        diccionario = {"nombre":self.nombre, "descripcion":self.descripcion, "id_usuario_creador":self.id_usuario_creador}
        return diccionario
    