from flask import Flask
from config import Config

from routes.usuarioBp import usuario_bp
from routes.servidorBp import servidor_bp
from routes.canalBp import canal_bp
from routes.mensajeBp import mensaje_bp

from routes.exceptionBp import errors

def init_app():

    app = Flask(__name__, static_folder = Config.STATIC_FOLDER,
                template_folder = Config.TEMPLATE_FOLDER)
    
    app.config.from_object(Config)

    #Rutas
    app.register_blueprint(usuario_bp)
    app.register_blueprint(servidor_bp)
    app.register_blueprint(canal_bp)
    app.register_blueprint(mensaje_bp)
    
    app.register_blueprint(errors)

    return app