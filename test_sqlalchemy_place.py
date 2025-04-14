from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.services.repositories.sqlalchemy_repository import SQLAlchemyRepository

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()

user_repo = SQLAlchemyRepository(User)
place_repo = SQLAlchemyRepository(Place)

user = User(
    first_name="PlaceOwner",
    last_name="Test",
    email="placeowner@example.com",
    password="hashed_password",
    is_admin=False
)
user_repo.add(user)
print(f"✅ User owner created: {user.id}")

place = Place(
    title="Test Place",
    description="Nice location",
    price=99.99,
    latitude=48.85,
    longitude=2.35,
    owner_id=user.id
)
place_repo.add(place)
print(f"🏠 Place created: {place.id}")

retrieved = place_repo.get(place.id)
print(f"📥 Place retrieved: {retrieved.title}")

place_repo.update(place.id, {"title": "Updated Place Title"})
updated = place_repo.get(place.id)
print(f"✏️ Place updated: {updated.title}")

place_repo.delete(place.id)
deleted = place_repo.get(place.id)
print(f"🗑️ Place deleted? {'Yes' if deleted is None else 'No'}")
