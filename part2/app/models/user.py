from app.models.base import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        if len(first_name) > 50 or len(last_name) > 50:
            raise ValueError("First and last name must be 50 characters or fewer")
        if '@' not in email:
            raise ValueError("Invalid email format")
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
