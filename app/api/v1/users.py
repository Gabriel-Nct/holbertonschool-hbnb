from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
import re

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='User password'),
    'is_admin': fields.Boolean(description='Admin flag')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address'),
    'password': fields.String(description='User password'),
    'is_admin': fields.Boolean(description='Admin flag')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input or email already exists')
    def post(self):
        """Create a new user (public access)"""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        errors = []
        if not user_data.get('first_name') or user_data['first_name'].strip() == "":
            errors.append("First name cannot be empty")
        if not user_data.get('last_name') or user_data['last_name'].strip() == "":
            errors.append("Last name cannot be empty")
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not user_data.get('email') or not re.match(email_pattern, user_data['email']):
            errors.append("Invalid email format")
        if not user_data.get('password') or len(user_data['password']) < 6:
            errors.append("Password must be at least 6 characters long")

        if errors:
            return {'error': 'Invalid input data', 'details': errors}, 400

        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'is_admin': new_user.is_admin
        }, 201

    @api.response(200, 'User list retrieved successfully')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def get(self):
        """Get list of all users (admin only)"""
        user_id = get_jwt_identity()
        user = facade.get_user(user_id)

        if not user or not user.is_admin:
            return {'error': 'Admin privileges required'}, 403

        users = facade.user_repo.get_all()
        return [{
            'id': u.id,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
            'is_admin': u.is_admin
        } for u in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @api.response(403, 'Access denied')
    @jwt_required()
    def get(self, user_id):
        """Get user details by ID (owner or admin only)"""
        current_user_id = get_jwt_identity()
        user = facade.get_user(current_user_id)

        if not user or (str(user.id) != str(user_id) and not user.is_admin):
            return {'error': 'Access denied'}, 403

        target_user = facade.get_user(user_id)
        if not target_user:
            return {'error': 'User not found'}, 404

        return {
            'id': target_user.id,
            'first_name': target_user.first_name,
            'last_name': target_user.last_name,
            'email': target_user.email,
            'is_admin': target_user.is_admin
        }, 200

    @api.expect(user_update_model)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update user information (owner or admin only)"""
        current_user_id = get_jwt_identity()
        user = facade.get_user(current_user_id)
        user_data = api.payload

        if not user:
            return {'error': 'Unauthorized action'}, 403

        is_admin = user.is_admin
        is_self = str(user.id) == str(user_id)

        if not is_self and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        if not is_admin and ('email' in user_data or 'password' in user_data):
            return {'error': 'You cannot modify email or password'}, 400

        if is_admin and 'email' in user_data:
            existing = facade.get_user_by_email(user_data['email'])
            if existing and existing.id != user_id:
                return {'error': 'Email is already in use'}, 400

        if 'first_name' in user_data and (not user_data['first_name'].strip()):
            return {'error': 'First name cannot be empty'}, 400
        if 'last_name' in user_data and (not user_data['last_name'].strip()):
            return {'error': 'Last name cannot be empty'}, 400
        if 'email' in user_data:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, user_data['email']):
                return {'error': 'Invalid email format'}, 400
        if 'password' in user_data and len(user_data['password']) < 6:
            return {'error': 'Password must be at least 6 characters long'}, 400

        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User not found'}, 404

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email,
            'is_admin': updated_user.is_admin
        }, 200
