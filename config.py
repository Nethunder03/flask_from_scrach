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
    'uiversion': 3,
    'description': 'Documentation de l\'API avec Flask et Swagger',
    'version': '1.0.0',
    'contact': {
        'name': 'Rock Ferrand MALELA',
        'email': 'guyrockmalela@gmail.com',
    },
    'specs': [
        {
            'endpoint': 'apispec',
            'route': '/apispec.json',  # Ceci est la route où le fichier JSON est exposé
            'rule_filter': lambda rule: True,
            'model_filter': lambda tag: True,
        }
    ],
    'static_url_path': '/flasgger_static',
    'swagger_ui': True,
    'specs_route': '/apidocs/',  # URL pour accéder à Swagger UI
    'swagger_url': '/Schemas/',  # Chemin pour accéder au fichier JSON statique
}

    JWT_SECRET_KEY = 'your-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 86400