from flask import Blueprint

from controllers.controladorMensaje import ControladorMensaje

mensaje_bp = Blueprint('mensaje_bp',__name__)

mensaje_bp.route('/mensajes/', methods = ['POST'])(ControladorMensaje.crear_mensaje)

mensaje_bp.route('/mensajes/<int:id_mensaje>', methods = ['GET'])(ControladorMensaje.get_mensaje)

mensaje_bp.route('/mensajes/', methods = ['PUT'])(ControladorMensaje.editar_mensaje)

mensaje_bp.route('/mensajes/<int:id_mensaje>', methods = ['DELETE'])(ControladorMensaje.eliminar_mensaje)