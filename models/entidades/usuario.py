from models.baseDeDatos import BaseDeDatos  

class Usuario:
    def __init__(self, nombre:str, apellido:str, alias:str, correo:str,
                 password:str, tipo_estado = 1, codigo_verificacion:str = None, id_usuario:int = None):
        self.nombre = nombre
        self.apellido = apellido
        self.alias = alias
        self.correo = correo
        self.password = password
        self.tipo_estado = tipo_estado
        self.codigo_verificacion = codigo_verificacion
        self.id_usuario = id_usuario
    
    @classmethod
    def crear_usuario(cls, usuario):
        consulta = """INSERT INTO mootmate.usuario
        (nombre, apellido, alias, email, password, codigo_verificacion)
        values (%s,%s,%s,%s,%s,%s,%s)"""
        parametros = (  usuario.nombre,
                        usuario.apellido,
                        usuario.alias,
                        usuario.correo,
                        usuario.password,
                        usuario.tipo_estado,
                        usuario.codigo_verificacion)
        BaseDeDatos.ejecutar_consulta(consulta, parametros)
    
    @classmethod
    def get_usuario(cls, id_usuario:int):
        consulta = """SELECT * FROM mootmate.usuarios as u
        WHERE u.id_usuario = %s"""
        response = BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=id_usuario, diccionario=True)
        id_estado = response.pop("id_tipo_estado")
        consulta = """SELECT * FROM mootmate.tipo_estado as t_e WHERE t_e.id_tipo_estado = %s"""
        tipo_estado = BaseDeDatos.traer_uno(consulta=consulta, parametros=id_estado, diccionario=True)
        response["Estado"] = tipo_estado
        return response
    
    @classmethod
    def get_servidores(cls, id_usuario:int):
        consulta = """SELECT s.id_servidor, s.nombre, s.descripcion, s.fecha_creacion
        FROM usuarios as u INNER JOIN usuarios_servidores as u_s ON u.id_usuario = u_s.id_usuario
        INNER JOIN servidores as s ON u_s.id_servidor = s.id_servidor
        WHERE u.id_usuario = %s"""
        return BaseDeDatos.traer_todo(consulta=consulta, parametros=id_usuario, diccionario=True)

    @classmethod
    def get_privilegio(cls, id_usuario, id_servidor):
        consulta = """SELECT p_u.id_privilegio_usuario, p_u.nombre
        FROM usuarios_servidores as u_s INNER JOIN privilegios_usuario as p_u
        ON u_s.id_privilegio_usuario = p_u..id_privilegio_usuario
        WHERE u_s.id_usuario = %s AND u_s.id_servidor = %s"""
        return BaseDeDatos.traer_uno(consulta=consulta, parametros=(id_servidor,id_servidor), diccionario=True)

    @classmethod
    def get_usuarios(cls):
        consulta = """SELECT * FROM mootmate.usuarios"""
        response = BaseDeDatos.traer_todo(consulta=consulta,diccionario=True)
        usuarios = []
        for usuario in response:
            id_estado = usuario.pop("id_tipo_estado")
            consulta = """SELECT * FROM mootmate.tipo_estado as t_e WHERE t_e.id_tipo_estado = %s"""
            tipo_estado = BaseDeDatos.traer_uno(consulta=consulta, parametros=id_estado, diccionario=True)
            usuario["Estado"] = tipo_estado
            usuarios.append[usuario]
        return usuarios
    
    @classmethod
    def actualizar_usuario(cls, usuario):
        consulta = """UPDATE mootmate.usuarios as u SET
        u.nombre = %s,
        uapellido = %s,
        u.nombre_usuario = %s,
        u.correo = %s,
        u.contrasena = %s,
        u.id_tipo_estado = %s,
        u.codigo_verificacion = %s
        u.WHERE u.id_usuario = %s"""
        parametros = (  usuario.nombre,
                        usuario.apellido,
                        usuario.alias,
                        usuario.correo,
                        usuario.password,
                        usuario.tipo_estado,
                        usuario.codigo_verificacion,
                        usuario.id_usuario)
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=parametros)
    
    @classmethod
    def cambiar_estado(cls, id_usuario, id_tipo_estado):
        consulta = """UPDATE mootmate.usuarios as u SET u.id_tipo_estado = %s
        WHERE u.id_usuario = %s"""
        parametros = (id_tipo_estado,id_usuario)
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=parametros)

    @classmethod
    def eliminar_usuario(cls, id_usuario: int):
        #Supondremos que el id de tipo_de_estado de eliminado es 2
        cls.cambiar_estado(id_usuario, 2)
        
    @classmethod
    def existe_usuario(cls, id_usuario):
        consulta = """SELECT u.id_usuario FROM mootmate.usuarios as u WHERE u.id_usuario = %s"""
        response = BaseDeDatos.traer_uno(consulta=consulta,parametros=id_usuario)
        if response != None:
            return True
        else:
            return False
    
    @classmethod
    def agregar_servidor(cls, id_usuario, id_servidor):
        consulta = """INSERT INTO mootmate.usuarios_servidores (id_servidor, id_usuario)
        Values (%s,%s)"""
        parametros = (id_servidor, id_usuario)
        BaseDeDatos.ejecutar_consulta(consulta=consulta, parametros=parametros)
    
    @classmethod
    def usuario_eliminado(cls, id_usuario):
        respuesta = False
        consulta = """SELECT t_e.nombre FROM mootmate.usuarios as u
        INNER JOIN mootmate.tipo_estado as t_e ON u.id_tipo_estado = t_e.id_tipo_estado
        WHERE u.id_usuario = %s"""
        tipo_estado = BaseDeDatos.traer_uno(consulta=consulta, parametros=id_usuario)
        if tipo_estado[0] == "eliminado":
            respuesta = True
        return respuesta
        
    def serealizar_usuario(self):
        serial = {"nombre": self.nombre,
                  "apellido": self.apellido,
                  "alias": self.alias,
                  "correo": self.correo,
                  "password": self.password,
                  "id_tipo_estatado": self.tipo_estado,
                  "codigo_verificacion": self.codigo_verificacion,
                  "id": self.id_usuario}
        return serial