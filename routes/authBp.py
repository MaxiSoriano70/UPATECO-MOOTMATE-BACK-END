from flask import Blueprint
from controllers.auth_controller import UsuarioController

auth_bp = Blueprint('auth_bp', __name__)

auth_bp.route('/auth/login', methods=['POST'])(UsuarioController.login)
auth_bp.route('/auth/logout', methods=['GET'])(UsuarioController.logout)
auth_bp.route('/auth/register', methods=['POST'])(UsuarioController.crear_usuario)
auth_bp.route('/auth/get_user/<int:id_usuario>', methods=['GET'])(UsuarioController.get_user)
auth_bp.route('/auth/profile', methods=['GET'])(UsuarioController.perfil)