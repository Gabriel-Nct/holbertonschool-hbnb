import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from config import config 

app = create_app('development')

with app.app_context():
    db.create_all()
    print("✅ Tables SQLite créées avec succès dans development.db.")
