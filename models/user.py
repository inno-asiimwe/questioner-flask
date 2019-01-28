import uuid
import datetime
import jwt
from flask import current_app
from app import db
from flask_bcrypt import Bcrypt


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(256), default=str(uuid.uuid4()))
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    meetups = db.relationship(
        'Meetup',
        backref='Meetup',
        cascade='all, delete-orphan')

    def __init__(self, email, password):
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.uuid = uuid.uuid4()

    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_user_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def encode_jwt_token(self, uuid, email, id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=60),
                'iat': datetime.datetime.utcnow(),
                'sub': {
                    'userInfo': {
                        'uuid': uuid,
                        'email': email,
                        'id': id
                    }
                }
            }
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            return str(e)

    def decode_jwt_token(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config.get('SECRET')
            )
            if BlacklistToken.blacklisted(token):
                return 'Token was revoked login again'
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Expired token'
        except jwt.InvalidTokenError:
            return 'Invalid Token'


class BlacklistToken(db.Model):

    __tablename__ = 'blacklist_token'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, token):
        self.token = token

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<token: {}>'.format(self.token)

    @classmethod
    def blacklisted(cls, token):
        return cls.query.filter_by(token=str(token)).first()
