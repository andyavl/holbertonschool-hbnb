from app.models.base import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
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
