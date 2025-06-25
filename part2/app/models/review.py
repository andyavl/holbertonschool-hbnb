from app.models.base import BaseModel

class Review(BaseModel):
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
