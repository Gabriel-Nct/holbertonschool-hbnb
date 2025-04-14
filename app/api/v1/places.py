from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('places', description='Place operations')

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'user_id': fields.String(description='User ID')
})

place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True),
    'description': fields.String(),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True)
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(),
    'description': fields.String(),
    'price': fields.Float(),
    'latitude': fields.Float(),
    'longitude': fields.Float()
})

place_detail_model = api.model('PlaceDetail', {
    'id': fields.String(),
    'title': fields.String(),
    'description': fields.String(),
    'price': fields.Float(),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
    'owner_id': fields.String(),
    'owner': fields.Nested(user_model),
    'amenities': fields.List(fields.Nested(amenity_model)),
    'reviews': fields.List(fields.Nested(review_model))
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_input_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def post(self):
        """Register a new place (requires authentication)"""
        user_id = get_jwt_identity()
        data = request.get_json()
        data['owner_id'] = user_id

        errors = []

        if not data.get('title') or data['title'].strip() == "":
            errors.append("Title cannot be empty")
        elif len(data['title']) > 100:
            errors.append("Title too long (max 100 characters)")

        if not isinstance(data.get('price'), (int, float)) or data['price'] <= 0:
            errors.append("Price must be a positive number")

        if not isinstance(data.get('latitude'), (int, float)) or not -90 <= data['latitude'] <= 90:
            errors.append("Latitude must be between -90 and 90")

        if not isinstance(data.get('longitude'), (int, float)) or not -180 <= data['longitude'] <= 180:
            errors.append("Longitude must be between -180 and 180")

        if errors:
            return {'error': 'Invalid input data', 'details': errors}, 400

        try:
            new_place = facade.create_place(data)
            return new_place, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        return facade.get_all_places(), 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place_by_id(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place, 200

    @api.expect(place_update_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update a place (only owner or admin)"""
        user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        data = request.get_json()
        existing_place = facade.get_place_by_id(place_id)

        if not existing_place:
            return {'error': 'Place not found'}, 404

        if not is_admin and existing_place.get('owner_id') != user_id:
            return {'error': 'Unauthorized action'}, 403

        errors = []

        if 'title' in data:
            if not data['title'].strip():
                errors.append("Title cannot be empty")
            elif len(data['title']) > 100:
                errors.append("Title too long (max 100 characters)")

        if 'price' in data and (not isinstance(data['price'], (int, float)) or data['price'] <= 0):
            errors.append("Price must be a positive number")

        if 'latitude' in data and (not isinstance(data['latitude'], (int, float)) or not -90 <= data['latitude'] <= 90):
            errors.append("Latitude must be between -90 and 90")

        if 'longitude' in data and (not isinstance(data['longitude'], (int, float)) or not -180 <= data['longitude'] <= 180):
            errors.append("Longitude must be between -180 and 180")

        if errors:
            return {'error': 'Invalid input data', 'details': errors}, 400

        try:
            updated = facade.update_place(place_id, data)
            if not updated:
                return {'error': 'Update failed'}, 400
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
