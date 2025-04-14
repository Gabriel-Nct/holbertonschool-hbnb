from app import db
from sqlalchemy.orm import validates
from .base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity class that represents an amenity in the database.
    Inherits from BaseModel which provides common attributes and methods.
    """
    __tablename__ = 'amenities'

    name = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, name):
        """
        Initialize an Amenity instance with a name.
        """
        super().__init__()
        self.name = name

    @validates('name')
    def validate_name(self, key, name):
        """
        Validate the name of the amenity.
        Raises ValueError if name is empty or exceeds 100 characters.
        """
        if not name or name.strip() == "":
            raise ValueError("Amenity name cannot be empty")
        if len(name) > 100:
            raise ValueError("Amenity name must be a maximum of 100 characters")
        return name

    def update(self, updated_data):
        """
        Update the amenity instance with new data.
        """
        if 'name' in updated_data:
            self.name = self.validate_name('name', updated_data['name'])

    def to_dict(self):
        """
        Convert the Amenity instance to a dictionary representation.
        This is useful for serialization and API responses.
        Returns:
            dict: A dictionary representation of the Amenity instance.
        """
        return {
            'id': self.id,
            'name': self.name,
            'created_at': (
                self.created_at.isoformat() if self.created_at else None
            ),
            'updated_at': (
                self.updated_at.isoformat() if self.updated_at else None
            )
        }
