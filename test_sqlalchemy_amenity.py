from app import create_app, db
from app.models.amenity import Amenity
from app.services.repositories.sqlalchemy_repository import SQLAlchemyRepository
import uuid

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()

amenity_repo = SQLAlchemyRepository(Amenity)

amenity = Amenity(name="WiFi")
amenity_repo.add(amenity)
print(f"✅ Amenity ajouté : {amenity.id} - {amenity.name}")

retrieved = amenity_repo.get(amenity.id)
print(f"📥 Amenity récupéré : {retrieved.name}")

amenity_repo.update(amenity.id, {"name": "High-Speed WiFi"})
updated = amenity_repo.get(amenity.id)
print(f"✏️ Amenity modifié : {updated.name}")

amenity_repo.delete(amenity.id)
deleted = amenity_repo.get(amenity.id)
print(f"🗑️ Amenity supprimé ? => {'Yes' if not deleted else 'No'}")
