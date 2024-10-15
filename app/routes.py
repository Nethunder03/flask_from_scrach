from flask import Blueprint, jsonify, request, render_template
from . import db
from .models import User, Post, Comment, Category
from .schemas import UserSchema, PostSchema, CommentSchema, CategorySchema
from flask_jwt_extended import jwt_required
from flasgger import swag_from


api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def accueil():
    return render_template('index.html')

@api_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """
    Récupère la liste des utilisateurs
    """
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return jsonify(user_schema.dump(users))


@api_bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    """
    Récupère un utilisateur par son ID
    """
    user = User.query.get_or_404(id)
    user_schema = UserSchema()
    return jsonify(user_schema.dump(user))


@api_bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    """
    Met à jour un utilisateur
    """
    user = User.query.get_or_404(id)
    data = request.get_json()
    user_schema = UserSchema()
    updated_user = user_schema.load(data, instance=user, session=db.session)
    db.session.commit()
    return jsonify(user_schema.dump(updated_user))

@api_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    """
    Supprime un utilisateur
    """
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204



# Récupérer la liste des publications
@api_bp.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    """
    Récupère la liste des publications
    """
    posts = Post.query.all()
    post_schema = PostSchema(many=True)
    return jsonify(post_schema.dump(posts))


# Récupérer une publication par son ID
@api_bp.route('/posts/<int:id>', methods=['GET'])
@jwt_required()
def get_post(id):
    """
    Récupère une publication par son ID
    """
    post = Post.query.get_or_404(id)
    post_schema = PostSchema()
    return jsonify(post_schema.dump(post))


# Créer une nouvelle publication
@api_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    """
    Crée une nouvelle publication
    """
    data = request.get_json()
    post_schema = PostSchema()
    post_data = post_schema.load(data, session=db.session)
    new_post = Post(
        title = post_data.title,
        content = post_data.content,
        date_posted = post_data.date_posted,
        user_id = post_data.user_id,
        category_id = post_data.category_id
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify(post_schema.dump(new_post)), 201


# Mettre à jour une publication
@api_bp.route('/posts/<int:id>', methods=['PUT'])
@jwt_required()
def update_post(id):
    """
    Met à jour une publication existante
    """
    post = Post.query.get_or_404(id)
    data = request.get_json()
    post_schema = PostSchema()
    updated_post = post_schema.load(data, instance=post, session=db.session)
    db.session.commit()
    return jsonify(post_schema.dump(updated_post))


# Supprimer une publication
@api_bp.route('/posts/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    """
    Supprime une publication par son ID
    """
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return '', 204




# Récupérer la liste des commentaires
@api_bp.route('/comments', methods=['GET'])
@jwt_required()
def get_comments():
    """
    Récupère la liste des commentaires
    """
    comments = Comment.query.all()
    comment_schema = CommentSchema(many=True)
    return jsonify(comment_schema.dump(comments))


# Récupérer un commentaire par son ID
@api_bp.route('/comments/<int:id>', methods=['GET'])
@jwt_required()
def get_comment(id):
    """
    Récupère un commentaire par son ID
    """
    comment = Comment.query.get_or_404(id)
    comment_schema = CommentSchema()
    return jsonify(comment_schema.dump(comment))


# Créer un nouveau commentaire
@api_bp.route('/comments', methods=['POST'])
@jwt_required()
def create_comment():
    """
    Crée un nouveau commentaire
    """
    data = request.get_json()
    comment_schema = CommentSchema()
    comment_data = comment_schema.load(data, session=db.session)
    new_comment = Comment(
    content = comment_data.content,
    date_commented = comment_data.date_commented,
    user_id = comment_data.user_id,
    post_id = comment_data.post_id

    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify(comment_schema.dump(new_comment)), 201


# Mettre à jour un commentaire
@api_bp.route('/comments/<int:id>', methods=['PUT'])
@jwt_required()
def update_comment(id):
    """
    Met à jour un commentaire existant
    """
    comment = Comment.query.get_or_404(id)
    data = request.get_json()
    comment_schema = CommentSchema()
    updated_comment = comment_schema.load(data, instance=comment, session=db.session)
    db.session.commit()
    return jsonify(comment_schema.dump(updated_comment))


# Supprimer un commentaire
@api_bp.route('/comments/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id):
    """
    Supprime un commentaire par son ID
    """
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return '', 204



# Récupérer la liste des catégories
@api_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """
    Récupère la liste des catégories
    """
    categories = Category.query.all()
    category_schema = CategorySchema(many=True)
    return jsonify(category_schema.dump(categories))


# Créer une nouvelle catégorie
@api_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    """
    Crée une nouvelle catégorie
    """
    data = request.get_json()
    category_schema = CategorySchema()
    category_data = category_schema.load(data, session=db.session)
    new_category = Category(name = category_data.name)
    db.session.add(new_category)
    db.session.commit()
    return jsonify(category_schema.dump(new_category)), 201


# Mettre à jour une catégorie
@api_bp.route('/categories/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    """
    Met à jour une catégorie existante
    """
    category = Category.query.get_or_404(id)
    data = request.get_json()
    category_schema = CategorySchema()
    updated_category = category_schema.load(data, instance=category, session=db.session)
    db.session.commit()
    return jsonify(category_schema.dump(updated_category))


# Supprimer une catégorie
@api_bp.route('/categories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    """
    Supprime une catégorie par son ID
    """
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return '', 204
