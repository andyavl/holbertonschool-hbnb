from app.extensions import db
from app.models.base_model import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String, db.ForeignKey('places.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='reviews')
    place = db.relationship('Place', back_populates='reviews')

    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text.strip():
            raise ValueError("Review text cannot be empty")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
