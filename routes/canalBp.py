from flask import Blueprint

from controllers.controladorCanal import ControladorCanal

canal_bp = Blueprint('canal_bp',__name__)

canal_bp.route('/canales/', methods = ['POST'])(ControladorCanal.crear_canal)

canal_bp.route('/canales/<int:id_canal>', methods = ['GET'])(ControladorCanal.get_canal)
canal_bp.route('/canales/mensajes', methods = ['GET'])(ControladorCanal.get_mensajes)

canal_bp.route('/canales/', methods = ['PUT'])(ControladorCanal.editar_canal)

canal_bp.route('/canales/<int:id_canal>', methods = ['DELETE'])(ControladorCanal.eliminar_canal)