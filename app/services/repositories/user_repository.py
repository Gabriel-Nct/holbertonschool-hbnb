from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """
    User repository for managing user data in the database.
    This class provides methods to interact with the User model,
    including creating, updating, deleting, and querying user records.
    """

    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """
        Get a user by their email address.
        """
        return self.model.query.filter_by(email=email).first()

    def save(self):
        """
        Save changes to the database.
        This method is used to commit the current session,
        ensuring that all changes made to the user records are persisted.
        This is a placeholder method and should be implemented
        in the context of your application.
        """
        from app import db
        db.session.commit()
