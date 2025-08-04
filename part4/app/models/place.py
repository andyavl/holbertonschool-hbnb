from app.extensions import db
from app.models.base_model import BaseModel


place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(60), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(60), db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)

    # One-to-many relationship: Place.owner points to User
    owner = db.relationship('User', back_populates='places')

    # One place can have many reviews
    reviews = db.relationship('Review', back_populates='place', cascade='all, delete-orphan')

    # Many-to-many relationship with amenities via association table
    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        back_populates='places',
        lazy='dynamic'
    )

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        if not title.strip():
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError("Title must be 100 characters or fewer")
        if price < 0:
            raise ValueError("Price must be positive")
        if not -90.0 <= latitude <= 90.0:
            raise ValueError("Latitude out of range")
        if not -180.0 <= longitude <= 180.0:
            raise ValueError("Longitude out of range")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)
