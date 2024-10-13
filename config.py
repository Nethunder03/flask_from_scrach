from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    FLASK_APP=os.getenv("FLASK_APP")
    FLASK_DEBUG=os.getenv("FLASK_DEBUG")
    FLASK_ENV=os.getenv("FLASK_ENV")
    SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI")
    SWAGGER = {
        'title': 'Ferrand MALELA API avec Flask et Swagger',
        'uiversion': 3,  # Changé de 3 à 2
        'description': 'Documentation de l\'API avec Flask et Swagger',
        'version': '1.0.0',
        'contact': {
            'name': 'Rock Ferrand MALELA',
            'email': 'guyrockmalela@gmail.com',
        },
        'specs': [
            {
                'endpoint': 'apispec',
                'route': '/apispec.json',
                'rule_filter': lambda rule: True,  # all in
                'model_filter': lambda tag: True,  # all in
            }
        ],
        'static_url_path': '/flasgger_static',
        'swagger_ui': True,
        'specs_route': '/apidocs/'
    }
    JWT_SECRET_KEY = 'your-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 86400