from models.baseDeDatos import BaseDeDatos  

class Mensaje:
    def __init__(self, mensaje, id_canal,
                 id_usuario, id_mensaje_relacionado = None,
                 borrado=False, editado=False, id_mensaje = None):
        self.mensaje = mensaje
        self.id_canal = id_canal
        self.id_usuario = id_usuario
        self.id_mensaje_relacionado = id_mensaje_relacionado
        self.id_mensaje = id_mensaje

    @classmethod    
    def crear_mensaje(cls, mensaje) -> None:
        consulta = """INSERT INTO mootmate.mensajes 
        (mensaje, id_canal, id_usuario, id_mensaje_relacionado) VALUES
        (%s, %s, %s, %s)"""
        parametros = (mensaje.mensaje, mensaje.id_canal, mensaje.id_usuario, mensaje.id_mensaje_relacionado)
        cursor = BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=parametros)
        mensaje.id_mensaje = cursor.lastrowid

    @classmethod
    def get_mensaje(cls, id_mensaje) -> dict:
        consulta = """SELECT * FROM mootmate.mensajes as m WHERE m.id_mensaje = %s"""
        respuesta = BaseDeDatos.traer_uno(consulta=consulta, parametros=id_mensaje, diccionario=True)
        return respuesta
        
    #metodo si se agrega la funcion de editar mensaje
    @classmethod
    def get_mensajes_viejos(cls, id_mensaje) -> tuple:
        consulta = """SELECT * FROM mootmate.mensajes_viejos AS m_v
        INNER JOIN mootmate.mensajes AS m ON m_v.id_mensaje_actual = m.id_mensaje
        WHERE m.id_mensaje = %s
        ORDER BY m_v.fecha_creacion DESC"""
        respuesta = BaseDeDatos.traer_todo(consulta=consulta, parametros=id_mensaje, diccionario=True)
        return respuesta

    @classmethod
    def editar_mensaje(cls, mensaje) -> None:
        viejo = cls.get_mensaje(mensaje.id_mensaje)
        consulta = """INSERT INTO mootmate.mensajes_viejos (id_mensaje_actual, mensaje)
        values (%s, %s)"""
        parametros = (mensaje.id_mensaje, viejo["mensaje"])
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=parametros)
        consulta = """UPDATE mootmate.mensajes as m SET
        m.mensaje = %s,
        m.editado = 1
        WHERE m.id_mensaje = %s"""
        parametros = (mensaje.mensaje, mensaje.id_mensaje)
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=parametros)
    
    @classmethod
    def eliminar_mensaje(cls, id_mensaje) -> None:
        consulta = """UPDATE mootmate.mensajes as m SET m.borrado = 1 WHERE m.id_mensaje = %s"""
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=id_mensaje)
    
    @classmethod
    def existe_mensaje(cls, id_mensaje) -> bool:
        consulta = """SELECT m.id_mensaje FROM mootmate.mensajes as m WHERE m.id_mensaje = %s"""
        return BaseDeDatos.traer_uno(consulta=consulta, parametros=id_mensaje) != None
