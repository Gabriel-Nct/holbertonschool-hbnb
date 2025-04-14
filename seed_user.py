import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.user import User

app = create_app('development')

with app.app_context():
    user = User.query.filter_by(email="test@example.com").first()
    if not user:
        new_user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="testpassword",
            is_admin=True
        )
        db.session.add(new_user)
        db.session.commit()
        print("✅ Utilisateur de test créé avec succès.")
    else:
        print("ℹ️ Utilisateur de test déjà présent.")
