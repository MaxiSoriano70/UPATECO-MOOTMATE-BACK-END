from flask import Blueprint

from models.exceptions import BadRequest, DataBaseError, UsuarioNoEncontrado, CanalNoEncontrado, MensajeNoEncontrado, ServidorNoEncontrado

errors = Blueprint("errors", __name__)

@errors.app_errorhandler(BadRequest)
def handle_bad_request(error):
    return error.get_response()

@errors.app_errorhandler(DataBaseError)
def handle_data_base_error(error):
    return error.get_response()

@errors.app_errorhandler(UsuarioNoEncontrado)
def handle_usuario_no_encontrado(error):
    return error.get_response()

@errors.app_errorhandler(CanalNoEncontrado)
def handle_canal_no_encontrado(error):
    return error.get_response()

@errors.app_errorhandler(ServidorNoEncontrado)
def handle_servidor_no_encontrado(error):
    return error.get_response()

@errors.app_errorhandler(MensajeNoEncontrado)
def handle_mensaje_no_encontrado(error):
    return error.get_response()