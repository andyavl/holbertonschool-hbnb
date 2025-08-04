from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.utils.auth import is_admin


api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Admin-only: Register a new user"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.marshal_list_with(user_model)
    def get(self):
        """Get list of all users"""
        users = facade.get_all_users()
        return users, 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @jwt_required()
    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user by ID — admin or user themselves"""
        current_user_id = get_jwt_identity()
        is_admin_user = is_admin()

        if not is_admin_user and user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        data = api.payload
        email = data.get('email')
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        updated = facade.update_user(user_id, data)
        if not updated:
            return {'error': 'User not found'}, 404

        return {
            'id': updated.id,
            'first_name': updated.first_name,
            'last_name': updated.last_name,
            'email': updated.email
        }, 200

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()  # This will be the string user ID
        claims = get_jwt()            # This is a dict containing any additional_claims

        return {
            'message': f'Hello, user {user_id}',
            'is_admin': claims.get('is_admin')
        }, 200
