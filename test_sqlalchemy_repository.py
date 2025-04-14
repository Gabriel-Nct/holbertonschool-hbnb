from app import create_app, db
from app.models.place import Place
from app.services.repositories.sqlalchemy_repository import SQLAlchemyRepository

app = create_app()

with app.app_context():

    db.drop_all()
    db.create_all()

    repo = SQLAlchemyRepository(Place)

    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "secretpass"
    }
    user = User(**user_data)
    repo.add(user)
    print("✅ User ajouté :", user)

    retrieved = repo.get(user.id)
    print("📥 User récupéré :", retrieved)

    repo.update(user.id, {"first_name": "Updated"})
    updated = repo.get(user.id)
    print("✏️ User modifié :", updated)

    repo.delete(user.id)
    deleted = repo.get(user.id)
    print("🗑️ User supprimé ? =>", deleted is None)
