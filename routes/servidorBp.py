from flask import Blueprint

from controllers.controladorServidor import ControladorServidor

servidor_bp = Blueprint('servidor_bp',__name__)

servidor_bp.route('/servidores/', methods = ['POST'])(ControladorServidor.crear_servidor)

servidor_bp.route('/servidores/<int:id_servidor>', methods = ['GET'])(ControladorServidor.get_servidor)
servidor_bp.route('/servidores/<int:id_servidor>/creador/', methods = ['GET'])(ControladorServidor.get_usuario_creador)
servidor_bp.route('/servidores/<int:id_servidor>/usuarios/', methods = ['GET'])(ControladorServidor.get_usuarios)
servidor_bp.route('/servidores/<int:id_servidor>/canales/', methods = ['GET'])(ControladorServidor.get_canales)

servidor_bp.route('/servidores/', methods = ['PUT'])(ControladorServidor.editar_servidor)

servidor_bp.route('/servidores/<int:id_servidor>', methods = ['DELETE'])(ControladorServidor.eliminar_servidor)
servidor_bp.route('/servidores/<int:id_servidor>/usuarios/<int:id_usuario>', methods = ['DELETE'])(ControladorServidor.eliminar_usuario)