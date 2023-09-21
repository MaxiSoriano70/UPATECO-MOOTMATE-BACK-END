from models.baseDeDatos import BaseDeDatos  

class Canal:
    def __init__(self, nombre, descripcion, id_servidor, id_canal=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.id_servidor = id_servidor
        self.id_canal = id_canal
    
    @classmethod
    def crear_canal(cls, canal):
        consulta = """INSERT INTO mootmate.canales (nombre, id_servidor, descripcion)
        VALUES (%s, %s, %s)"""
        parametros = (canal.nombre, canal.id_servidor, canal.descripcion)
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=parametros)


    @classmethod
    def get_canal(cls, id_canal) -> dict:
        consulta = """SELECT * FROM mootmate.canales as c WHERE c.id_canal = %s"""
        respuesta = BaseDeDatos.traer_uno(consulta=consulta, parametros=id_canal)
        return respuesta

    @classmethod
    def get_mensajes(cls, id_canal) -> list:
        consulta = """SELECT * FROM mootmate.mensajes as m WHERE m.id_canal = %s
        ORDER BY m.fecha_creacion ASC"""
        respuesta = BaseDeDatos.traer_todo(consulta=consulta, parametros=id_canal, diccionario=True)
        mensajes = {"mensajes":respuesta}
        return mensajes

    @classmethod
    def editar_canal(cls, canal):
        consulta = """UPDATE mootmate.canales as c SET
        c.nombre = %s,
        c.descripcion = %s
        WHERE c.id_canal = %s"""
        parametros = (canal.nombre, canal.descripcion, canal.id_canal)
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=parametros)

    @classmethod
    def eliminar_canal(cls, id_canal):
        consulta = """DELETE FROM mootmate.canales as c WHERE c.id_canal = %s"""
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=id_canal)

    @classmethod
    def existe_canal(cls, id_canal):
        consulta = """SELECT id_canal FROM mootmate.canales as c WHERE c.id_canal = %s"""
        respuesta = BaseDeDatos.traer_uno(consulta=consulta, parametros=id_canal)
        if respuesta != None:
            return True
        else:
            return False
