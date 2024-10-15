from flask import Flask
from config import Config
from extensions import db, migrate, ma, jwt
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from .routes import api_bp

    app.register_blueprint(api_bp)
    Swagger(app, template_file='Schemas/swagger.json')
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    return app