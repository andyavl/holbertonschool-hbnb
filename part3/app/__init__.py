from flask import Flask
from flask_restx import Api
from app.extensions import db, bcrypt, jwt
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns

from config import DevelopmentConfig
from flask_jwt_extended import JWTManager


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    # Create admin only inside app context
    with app.app_context():
        db.create_all()
        from app.services import facade
        existing_admin = facade.get_user_by_email("admin@example.com")
        if not existing_admin:
            facade.create_user({
                "first_name": "Admin",
                "last_name": "User",
                "email": "admin@example.com",
                "password": "admin123",
                "is_admin": True
            })

    return app
