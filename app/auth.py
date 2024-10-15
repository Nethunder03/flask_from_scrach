from flask import Blueprint, request, jsonify
from extensions import db
from .models import User
from .schemas import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, unset_jwt_cookies, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Enregistrement d'un nouvel utilisateur.
    """
    data = request.get_json()
    user_schema = UserSchema()

    # Vérifier si l'utilisateur existe déjà
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email déjà utilisé"}), 400

    user = user_schema.load(data, session=db.session)
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password)
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authentifie un utilisateur et retourne les tokens JWT
    """
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'email': user.email})
        refresh_token = create_refresh_token(identity={'email': user.email})
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200

    return jsonify({"msg": "Identifiants incorrects"}), 401
  
  

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Déconnecte l'utilisateur en supprimant le token JWT.
    """
    try:
        # Récupération de l'identité du JWT
        current_user = get_jwt_identity()

        # Si un token valide est fourni, on peut déconnecter l'utilisateur
        if current_user:
            response = jsonify({"msg": "Déconnexion réussie"})
            unset_jwt_cookies(response)
            return response, 200
    except Exception as e:
        # Si un problème survient (token manquant ou invalide), on renvoie une erreur
        raise Unauthorized(description="Token invalide ou non fourni")