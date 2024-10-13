from app import ma
from app.models import User, Post, Comment, Category
from marshmallow import fields, validate, ValidationError

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    username = fields.String(
        required=True,
        validate=[
            validate.Length(min=3, max=50),
            validate.Regexp(r'^[a-zA-Z0-9_]+$',
                            error="Le nom d'utilisateur ne peut contenir que des lettres, chiffres et underscores")
        ],
        error_messages={
            'required': 'Le nom d\'utilisateur est requis.',
            'invalid': 'Le format du nom d\'utilisateur est invalide.'
        }
    )

    email = fields.Email(
        required=True,
        validate=validate.Length(max=120),
        error_messages={
            'required': 'L\'email est requis.',
            'invalid': 'L\'email doit être valide.'
        }
    )

    password = fields.String(
        required=True,
        validate=[
            validate.Length(min=8),
            validate.Regexp(r'[A-Za-z0-9@#$%^&+=]',
                            error="Le mot de passe doit contenir au moins un caractère spécial.")
        ],
        error_messages={
            'required': 'Le mot de passe est requis.',
            'invalid': 'Le mot de passe ne respecte pas les critères de sécurité.'
        }
    )

    created_at = fields.DateTime(dump_only=True)



class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True

    title = fields.String(
        required=True,
        validate=[
            validate.Length(min=3, max=120),
        ],
        error_messages={
            'required': 'Le titre est requis.',
            'invalid': 'Le titre doit avoir entre 3 et 120 caractères.'
        }
    )

    content = fields.String(
        required=True,
        validate=[
            validate.Length(min=10),
        ],
        error_messages={
            'required': 'Le contenu est requis.',
            'invalid': 'Le contenu doit avoir au moins 10 caractères.'
        }
    )

    date_posted = fields.DateTime(dump_only=True)

    user_id = fields.Integer(
        required=True,
        error_messages={
            'required': 'L\'utilisateur est requis.',
            'invalid': 'ID utilisateur invalide.'
        }
    )

    category_id = fields.Integer(
        allow_none=True,
        error_messages={
            'invalid': 'ID de catégorie invalide.'
        }
    )


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        load_instance = True

    content = fields.String(
        required=True,
        validate=[
            validate.Length(min=5),
        ],
        error_messages={
            'required': 'Le contenu du commentaire est requis.',
            'invalid': 'Le commentaire doit contenir au moins 5 caractères.'
        }
    )

    date_commented = fields.DateTime(dump_only=True)

    user_id = fields.Integer(
        required=True,
        error_messages={
            'required': 'L\'utilisateur est requis.',
            'invalid': 'ID utilisateur invalide.'
        }
    )

    post_id = fields.Integer(
        required=True,
        error_messages={
            'required': 'L\'article est requis.',
            'invalid': 'ID d\'article invalide.'
        }
    )


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True


    name = fields.String(
        required=True,
        validate=[
            validate.Length(min=3, max=100),
            validate.Regexp(r'^[a-zA-Z0-9_ ]+$',
                            error="Le nom de la catégorie ne peut contenir que des lettres, chiffres et espaces")
        ],
        error_messages={
            'required': 'Le nom de la catégorie est requis.',
            'invalid': 'Le nom de la catégorie doit avoir entre 3 et 100 caractères et contenir uniquement des lettres, chiffres et espaces.'
        }
    )


