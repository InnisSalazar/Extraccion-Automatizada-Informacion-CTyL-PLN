from flask import Flask
from src.routes.upload import upload_routes

def create_app():
    """
    Configura y retorna la aplicación Flask.
    """
    app = Flask(__name__, template_folder='/app/templates', static_folder='/app/static')
    app.config['UPLOAD_FOLDER'] = '/app/uploads'

    # Registrar las rutas desde los módulos
    app.register_blueprint(upload_routes)

    return app
