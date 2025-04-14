from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.services.repositories.sqlalchemy_repository import SQLAlchemyRepository
import uuid

app = create_app("development")

with app.app_context():
    db.drop_all()
    db.create_all()

    user_repo = SQLAlchemyRepository(User)
    place_repo = SQLAlchemyRepository(Place)
    review_repo = SQLAlchemyRepository(Review)

    user = User(
    first_name="John",
    last_name="Doe",
    email="johndoe@example.com"
)
    user.hash_password("password123")
    user_repo.add(user)

    print(f"✅ User created: {user.id}")

    place = Place(
        title="Lovely Apartment",
        description="A nice place",
        price=100,
        latitude=48.8566,
        longitude=2.3522,
        owner_id=user.id
    )
    place_repo.add(place)
    print(f"🏠 Place created: {place.id}")

    review = Review(
        text="Really enjoyed it!",
        rating=5,
        place_id=place.id,
        user_id=user.id
    )
    review_repo.add(review)
    print(f"📝 Review added: {review.id}")

    fetched = review_repo.get(review.id)
    print(f"📥 Review text: {fetched.text}")

    review_repo.update(review.id, {"text": "It was fantastic!"})
    print(f"✏️ Updated review: {review_repo.get(review.id).text}")

    review_repo.delete(review.id)
    deleted = review_repo.get(review.id) is None
    print(f"🗑️ Review deleted? => {deleted}")
