import mysql.connector

from config import Config

from datetime import datetime

class BaseDeDatos:
    _coneccion = None

    @classmethod
    def conectarse(cls):
        if cls._coneccion == None:
            cls._coneccion = mysql.connector.connect(**Config._credenciales)
        return cls._coneccion
    
    @classmethod
    def ejecutar_consulta(cls, consulta, parametros=None, formato=None, diccionario=False):
        cursor = cls.conectarse().cursor(dictionary=diccionario)
        if parametros != None:
            try:
                iter(parametros)
                if not(isinstance(parametros,str)):
                    if isinstance(parametros, datetime):
                        try:
                            cursor.execute(consulta, parametros.strftime(formato))
                        except:
                            cursor.execute(consulta, parametros.strftime("%Y-%m-%d"))
                    else:
                        cursor.execute(consulta, parametros)
                else:
                    cursor.execute(consulta, (parametros, ))
            except TypeError:
                cursor.execute(consulta, (str(parametros), ))
        return cursor
    
    @classmethod
    def traer_uno(cls, consulta, parametros=None, formato=None, diccionario = False):
        cursor = cls.ejecutar_consulta(consulta, parametros, formato, diccionario)
        return cursor.fetchone()
    
    def traer_todo(cls, consulta, parametros, formato=None, diccionario = False):
        cursor = cls.ejecutar_consulta(consulta, parametros, formato, diccionario)
        return cursor.fetchall()