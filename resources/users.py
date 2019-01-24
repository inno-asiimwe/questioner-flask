from flask import Blueprint
from flask_restful import (Resource, reqparse,
                           Api, marshal, marshal_with,
                           fields)
from models.user import User


user_fields = {
    'id': fields.Integer,
    'uuid': fields.String,
    'email': fields.String,
}


class UserRegistration(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            type=str,
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            type=str,
            required=True,
            location=['form', 'json']
        )

    def post(self):

        args = self.reqparse.parse_args()

        if not User.find_user_by_email(args.get('email')):
            user = User(**args)

            try:
                user.save()
            except Exception as e:
                return {'message': str(e)}, 400

            return {'user': marshal(user, user_fields)}, 201
        return {"message": "email already registered"}, 409


class UserLogin(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            type=str,
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            type=str,
            required=True,
            location=['form', 'json']
        )

    def post(self):

        args = self.reqparse.parse_args()
        current_user = User.find_user_by_email(args.get('email'))

        if current_user and current_user.password_is_valid(
                args.get('password')):

            token = current_user.encode_jwt_token(
                current_user.uuid, current_user.email)
            return {
                'message': "Successfully logged in",
                'token': token.decode()}, 200
        return {'message': 'Login failed'}, 401


auth_api = Blueprint('resources.user', __name__)
api = Api(auth_api, catch_all_404s=True)
api.add_resource(
    UserRegistration,
    '/register',
    endpoint='registration'
)
api.add_resource(
    UserLogin,
    '/login',
    endpoint='login'
)
