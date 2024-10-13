import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from app import create_app, db
from app.models import User, Post, Comment, Category
from app.schemas import UserSchema, PostSchema, CommentSchema, CategorySchema

@pytest.fixture(scope="module")
def app():
    """
    Configure l'application Flask pour les tests.
    Utilise une base de données SQLite en mémoire pour les tests.
    """
    app = create_app()

    # Configurations pour les tests
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Base SQLite en mémoire
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope="module")
def client(app):
    """
    Fournit un client de test pour envoyer des requêtes HTTP à l'application.
    """
    return app.test_client()


@pytest.fixture(scope="module")
def create_user():
    """
    Crée un utilisateur de test pour simuler un utilisateur authentifié.
    """
    user = User(username="testuser", email="testuser@example.com", password="testpassword")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture(scope="module")
def auth_headers(create_user):
    """
    Génère un token JWT pour simuler un utilisateur authentifié.
    """
    token = create_access_token(identity=create_user.id)
    return {
        "Authorization": f"Bearer {token}"
    }



# Tests pour les utilisateurs

def test_get_users(client, auth_headers, create_user):
    response = client.get('/users', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['username'] == "testuser"

def test_get_user(client, auth_headers, create_user):
    response = client.get(f'/users/{create_user.id}', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['username'] == "testuser"

def test_update_user(client, auth_headers, create_user):
    data = {
        "username": "updateduser",
        "email": "updated@example.com",
        "password": "newpassword"
    }
    response = client.put(f'/users/{create_user.id}', json=data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json['username'] == "updateduser"
    assert response.json['email'] == "updated@example.com"

def test_delete_user(client, auth_headers, create_user):
    response = client.delete(f'/users/{create_user.id}', headers=auth_headers)
    assert response.status_code == 204
    assert db.session.query(User).count() == 0

# Tests pour les publications

def test_create_post(client, auth_headers):
    data = {
        "title": "Test Post",
        "content": "This is a test post",
        "user_id": 1
    }
    response = client.post('/posts', json=data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json['title'] == "Test Post"
    assert response.json['content'] == "This is a test post"

def test_get_posts(client, auth_headers):
    response = client.get('/posts', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) > 0

def test_update_post(client, auth_headers):
    data = {
        "title": "Updated Post",
        "content": "This is an updated post"
    }
    post = Post.query.first()
    response = client.put(f'/posts/{post.id}', json=data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json['title'] == "Updated Post"
    assert response.json['content'] == "This is an updated post"

def test_delete_post(client, auth_headers):
    post = Post.query.first()
    response = client.delete(f'/posts/{post.id}', headers=auth_headers)
    assert response.status_code == 204
    assert db.session.query(Post).count() == 0

# Tests pour les commentaires

def test_create_comment(client, auth_headers):
    post = Post.query.first()
    data = {
        "content": "This is a comment",
        "post_id": post.id,
        "user_id": 1
    }
    response = client.post('/comments', json=data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json['content'] == "This is a comment"

def test_get_comments(client, auth_headers):
    response = client.get('/comments', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) > 0

def test_update_comment(client, auth_headers):
    comment = Comment.query.first()
    data = {
        "content": "Updated comment content"
    }
    response = client.put(f'/comments/{comment.id}', json=data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json['content'] == "Updated comment content"

def test_delete_comment(client, auth_headers):
    comment = Comment.query.first()
    response = client.delete(f'/comments/{comment.id}', headers=auth_headers)
    assert response.status_code == 204
    assert db.session.query(Comment).count() == 0

# Tests pour les catégories

def test_create_category(client, auth_headers):
    data = {
        "name": "Test Category"
    }
    response = client.post('/categories', json=data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json['name'] == "Test Category"

def test_get_categories(client, auth_headers):
    response = client.get('/categories', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) > 0

def test_update_category(client, auth_headers):
    category = Category.query.first()
    data = {
        "name": "Updated Category"
    }
    response = client.put(f'/categories/{category.id}', json=data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json['name'] == "Updated Category"

def test_delete_category(client, auth_headers):
    category = Category.query.first()
    response = client.delete(f'/categories/{category.id}', headers=auth_headers)
    assert response.status_code == 204
    assert db.session.query(Category).count() == 0
