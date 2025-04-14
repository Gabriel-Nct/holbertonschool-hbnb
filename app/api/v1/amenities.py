from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new amenity (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        name = data.get('name', '').strip()

        if not name:
            return {
                'error': 'Invalid input data',
                'details': ['Amenity name cannot be empty']
            }, 400

        try:
            amenity = facade.create_amenity({'name': name})
            return {'id': amenity.id, 'name': amenity.name}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': a.id, 'name': a.name} for a in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's name (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        name = data.get('name', '').strip()

        if not name:
            return {
                'error': 'Invalid input data',
                'details': ['Amenity name cannot be empty']
            }, 400

        try:
            updated = facade.update_amenity(amenity_id, {'name': name})
            if not updated:
                return {'error': 'Amenity not found'}, 404
            return {'id': updated.id, 'name': updated.name}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
