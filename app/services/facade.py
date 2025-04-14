from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories.user_repository import UserRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)

    def create_user(self, user_data):
        """
        Create a new user with validation.
        Args:
            user_data (dict): User data containing email, password, and name
        Returns:
            User: Created user object
        """
        user = User(**user_data)
        if 'password' in user_data:
            user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieves a user by ID.
        Args:
            user_id (str): ID of the user to retrieve
        Returns:
            User: User object if found, None otherwise
        Raises:
            ValueError: If user ID is invalid
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Retrieves a user by email.
        Args:
            email (str): Email of the user to retrieve
        Returns:
            User: User object if found, None otherwise
        """
        return self.user_repo.get_user_by_email(
            email
        )  # Utilisation de la méthode spécifique

    def update_user(self, user_id, updated_data):
        """
        Updates the information of an existing user.
        Args:
            user_id (str): ID of the user to update
            updated_data (dict): Updated user data
        Returns:
            User: Updated user object or None if not found
        """
        self.user_repo.update(user_id, updated_data)
        return self.user_repo.get(user_id)

    def create_amenity(self, amenity_data):
        """
        Creates a new amenity with validation.
        Args:
            amenity_data (dict): Amenity data containing name
        Returns:
            Amenity: Created amenity object
        """
        name = amenity_data.get('name')

        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Retrieves an amenity by ID.
        Args:
            amenity_id (str): ID of the amenity to retrieve
        Returns:
            Amenity: Amenity object if found, None otherwise
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Retrieves all amenities.
        Returns:
            list: List of all amenities
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Updates an existing amenity's details.
        Args:
            amenity_id (str): ID of the amenity to update
            amenity_data (dict): Updated amenity data
        Returns:
            Amenity: Updated amenity object or None if not found
        """
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        if 'name' in amenity_data:
            self.amenity_repo.update(
                amenity_id, {'name': amenity_data['name']}
            )

        return self.amenity_repo.get(amenity_id)

    def create_place(self, place_data):
        """
        Creates a new place with validation and relationships.
        Args:
            place_data (dict): Place data containing title, description,
            price, latitude, longitude, and owner_id
        Returns:
            Place: Created place object
        """
        owner_id = place_data.get("owner_id")
        if not self.user_repo.get(owner_id):
            raise ValueError("Invalid owner ID.")

        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner_id=owner_id
        )

        if "amenities" in place_data and place_data["amenities"]:
            for amenity_id in place_data["amenities"]:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.add_amenity(amenity)

        self.place_repo.add(place)
        return place.to_dict()

    def get_place_by_id(self, place_id):
        """
        Retrieves a place by ID and loads its owner relationship.
        Args:
            place_id (str): ID of the place to retrieve
        Returns:
            dict: Place object in detailed format if found, None otherwise
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None

        place.owner = self.user_repo.get(place.owner_id)

        return place.to_detail_dict()

    def get_all_places(self):
        places = self.place_repo.get_all()
        for place in places:
            place.owner = self.user_repo.get(place.owner_id)
        return [place.to_summary_dict() for place in places]

    def update_place(self, place_id, place_data):
        """
        Updates an existing place with new data.
        Args:
            place_id (str): ID of the place to update
            place_data (dict): Updated place data
        Returns:
            bool: True if the update was successful, False otherwise
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None

        update_data = {}

        if "title" in place_data:
            update_data["title"] = place_data["title"]
        if "description" in place_data:
            update_data["description"] = place_data["description"]
        if "price" in place_data:
            update_data["price"] = place_data["price"]
        if "latitude" in place_data:
            update_data["latitude"] = place_data["latitude"]
        if "longitude" in place_data:
            update_data["longitude"] = place_data["longitude"]
        if "owner_id" in place_data:
            owner_id = place_data["owner_id"]
            if self.user_repo.get(owner_id):
                update_data["owner_id"] = owner_id

        if update_data:
            self.place_repo.update(place_id, update_data)

        place = self.place_repo.get(place_id)

        if "amenities" in place_data:
            place.amenities = []
            for amenity_id in place_data["amenities"]:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.add_amenity(amenity)

            self.place_repo.add(place)

        return True


    def create_review(self, review_data):
        """
        Create a new review with validation.
        Args:
            review_data (dict): Review data containing user_id, place_id,
            text, and rating
        Returns:
            Review: Created review object
        """
        if 'user_id' not in review_data:
            raise ValueError("user_id is required")
        if 'place_id' not in review_data:
            raise ValueError("place_id is required")
        if 'text' not in review_data or not review_data['text']:
            raise ValueError("text is required and cannot be empty")
        if 'rating' not in review_data:
            raise ValueError("rating is required")

        try:
            rating = float(review_data['rating'])
            if rating < 0 or rating > 5:
                raise ValueError("rating must be between 0 and 5")
        except (ValueError, TypeError):
            raise ValueError("rating must be a number between 0 and 5")

        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValueError(
                f"User with id {review_data['user_id']} does not exist"
            )

        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValueError(
                f"Place with id {review_data['place_id']} does not exist"
            )

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """
        Retrieve a review by ID.
        Args:
            review_id (str): ID of the review to retrieve
        Returns:
            Review: Review object if found, None otherwise
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Retrieve all reviews.
        Returns:
            list: List of all reviews
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews for a specific place.
        Args:
            place_id (str): ID of the place to retrieve reviews for
        Returns:
            list: List of reviews for the specified place
        """
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Place with id {place_id} does not exist")

        all_reviews = self.review_repo.get_all()
        return [
            review for review in all_reviews
            if review.place_id == place_id
        ]

    def update_review(self, review_id, review_data):
        """
        Update a review.

        Args:
            review_id (str): ID of the review to update
            review_data (dict): Updated review data

        Returns:
            Review: Updated review object

        Raises:
            ValueError: If review does not exist or validation fails
        """
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with id {review_id} does not exist")

        if 'rating' in review_data:
            try:
                rating = float(review_data['rating'])
                if rating < 0 or rating > 5:
                    raise ValueError("rating must be between 0 and 5")
                review_data['rating'] = rating
            except (ValueError, TypeError):
                raise ValueError("rating must be a number between 0 and 5")

        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        """
        Delete a review.

        Args:
            review_id (str): ID of the review to delete

        Returns:
            bool: True if successful, False otherwise

        Raises:
            ValueError: If review does not exist
        """
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with id {review_id} does not exist")

        self.review_repo.delete(review_id)
        return True
