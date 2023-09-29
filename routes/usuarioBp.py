from flask import Blueprint

from controllers.controladorUsuario import ControladorUsuario

usuario_bp = Blueprint('usuario_bp', __name__)

#POSTS
usuario_bp.route('/usuarios/', methods = ['POST'])(ControladorUsuario.crear_usuario)
#GETS
usuario_bp.route('/usuarios/', methods = ['GET'])(ControladorUsuario.get_usuarios)
usuario_bp.route('/usuarios/<int:id_usuario>', methods = ['GET'])(ControladorUsuario.get_usuario)
usuario_bp.route('/usuarios/<int:id_usuario>/servidores/', methods = ['GET'])(ControladorUsuario.get_servidores)
usuario_bp.route('/usuarios/<int:id_usuario>/servidores/<int:id_servidor>', methods = ['GET'])(ControladorUsuario.get_privilegio)
usuario_bp.route('/profile', methods=['GET'])(ControladorUsuario.show_profile)
usuario_bp.route('/logout', methods=['GET'])(ControladorUsuario.logout)
#PUTS
usuario_bp.route('/usuarios/foto/', methods = ['PUT'])(ControladorUsuario.actualizar_foto)
usuario_bp.route('/usuarios/', methods = ['PUT'])(ControladorUsuario.actualizar_usuario)
usuario_bp.route('/usuarios/<int:id_usuario>/servidores/<int:id_servidor>', methods = ['PUT'])(ControladorUsuario.agregar_servidor)
#DELETES
usuario_bp.route('/usuarios/<int:id_usuario>', methods = ['DELETE'])(ControladorUsuario.eliminar_usuario)

