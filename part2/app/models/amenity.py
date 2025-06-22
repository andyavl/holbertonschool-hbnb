from app.models.base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, description=""):
        super().__init__()
        if len(name) > 50:
            raise ValueError("Amenity name must be 50 characters or fewer")
        self.name = name
        self.description = description
