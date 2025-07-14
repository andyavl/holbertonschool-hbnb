from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        """Update timestamp before saving"""
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def update(self, data):
        """Update fields with a dictionary of values"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
