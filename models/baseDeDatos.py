import mysql.connector

from config import Config

from datetime import datetime

class BaseDeDatos:
    _conexion = None

    @classmethod
    def conectarse(cls):
        if cls._conexion == None:
            cls._conexion = mysql.connector.connect(**Config._credenciales)
        return cls._conexion
    
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
            
                
        else:
            cursor.execute(consulta)
        cls._conexion.commit()
        return cursor
    
    @classmethod
    def traer_uno(cls, consulta, parametros=None, formato=None, diccionario = False):
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
        else:
            cursor.execute(consulta)
        return cursor.fetchone()
    
    @classmethod
    def traer_todo(cls, consulta, parametros = None, formato=None, diccionario = False):
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
        else:
            cursor.execute(consulta)
        return cursor.fetchall()
    @classmethod
    def cerrar_conexion(cls):
        cls._conexion.close()