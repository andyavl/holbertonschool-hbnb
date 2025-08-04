from app.extensions import db, bcrypt
from app.models.base_model import BaseModel
import re


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # One user can own many places
    places = db.relationship('Place', back_populates='owner', cascade='all, delete-orphan')

    # One user can write many reviews
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()

        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required and must be 50 characters or fewer")

        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required and must be 50 characters or fewer")

        if not email or len(email) > 255 or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email must be valid and properly formatted")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        self.password = None
        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
