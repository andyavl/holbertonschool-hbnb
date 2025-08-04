from app.extensions import db
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String, nullable=True)

    # Many-to-many relationship back to Place
    places = db.relationship(
        'Place',
        secondary='place_amenity',
        back_populates='amenities',
        lazy='dynamic'
    )

    def __init__(self, name, description=""):
        super().__init__()
        if len(name) > 50:
            raise ValueError("Amenity name must be 50 characters or fewer")
        self.name = name
        self.description = description
