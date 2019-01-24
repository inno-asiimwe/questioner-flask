from functools import wraps
from flask import request, jsonify, make_response
from models.user import User


def auth_required(func):
    """decorator for authenticating a user using token based authentication """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        """ Decorated function for authenticating a user"""
        response = {
            'status': 'Failed',
            'message': 'Invalid token'
        }
        code = 401

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            auth_token = ''
        else:
            auth_token = auth_header.split(" ")[1]
            subject = User.decode_auth_token(auth_token)
        if not auth_token or isinstance(resp, str):
            return make_response(jsonify(response)), code
        user = {'user_info': subject, 'auth_token': auth_token}
        return func(user, *args, **kwargs)
    return decorated_function
