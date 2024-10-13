import json
import pytest
from app import create_app, db
from app.models import User
from flask_jwt_extended import create_access_token


@pytest.fixture
def app():
    """
    Configure l'application pour le test
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
        "JWT_SECRET_KEY": "test_secret",
    })
    with app.app_context():
        db.create_all()

    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Fournit un client pour envoyer des requêtes HTTP
    """
    return app.test_client()


@pytest.fixture
def register_user(client):
    """
    Enregistre un utilisateur pour les tests
    """
    response = client.post('/auth/register', json={
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'test_password'
    })
    assert response.status_code == 201
    return response.json


def test_register(client):
    """
    Teste la route d'enregistrement d'un utilisateur
    """
    response = client.post('/auth/register', json={
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'test_password'
    })
    assert response.status_code == 201
    assert 'username' in response.json
    assert 'email' in response.json


def test_register_duplicate(client, register_user):
    """
    Teste l'enregistrement avec un email déjà utilisé
    """
    response = client.post('/auth/register', json={
        'username': 'test_user2',
        'email': 'test@example.com',
        'password': 'test_password'
    })
    assert response.status_code == 400
    assert response.json['msg'] == 'Email déjà utilisé'


def test_login(client, register_user):
    """
    Teste la route de connexion
    """
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'test_password'
    })

    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json


def test_login_invalid_credentials(client, register_user):
    """
    Teste la connexion avec des identifiants invalides
    """
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'wrong_password'
    })

    assert response.status_code == 401
    assert response.json['msg'] == 'Identifiants incorrects'


def test_logout(client, register_user):
    """
    Teste la déconnexion de l'utilisateur
    """
    login_response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'test_password'
    })
    access_token = login_response.json['access_token']
    response = client.post('/auth/logout', headers={
        'Authorization': f'Bearer {access_token}'
    })

    assert response.status_code == 200
    assert response.json['msg'] == 'Déconnexion réussie'