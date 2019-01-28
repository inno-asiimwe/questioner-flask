import datetime
from flask import Blueprint
from flask_restful import (
    Resource, reqparse, Api, marshal, fields
)
from models.meetups import Meetup as meetup_model
from utils.users import auth_required


meetup_fields = {
    'uuid': fields.String,
    'created_on': fields.DateTime(dt_format='rfc822'),
    'topic': fields.String,
    'happening_on': fields.DateTime(dt_format='rfc822'),
    'location': fields.String,
    'created_by': fields.Integer
}


class MeetupList(Resource):
    decorators = [auth_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'topic',
            type=str,
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'happening_on',
            type=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'),
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'location',
            type=str,
            required=True,
            location=['form', 'json']
        )
        super().__init__()

    def get(self, user):
        all_meetups = meetup_model.get_all_meetups()

        if all_meetups:
            meetups = [marshal(meetup, meetup_fields)
                       for meetup in meetup_model.get_all_meetups()]
            return {'meetups': meetups}, 200
        return {'message': 'No meetups found'}, 200

    def post(self, user):

        args = self.reqparse.parse_args()
        topic = args.get('topic')
        location = args.get('location')
        happening_on = args.get('happening_on')
        created_by = user.get('user_info').get('userInfo').get('id')

        if not meetup_model.meetup_exists(topic, location, happening_on):
            meetup = meetup_model(created_by=created_by, **args)
            try:
                meetup.save()
                return {'meetup': marshal(meetup, meetup_fields)}, 201
            except Exception as e:
                return {'error': str(e)}, 400
        return {'message': 'Meetup already exists'}, 409


class Meetup(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'topic',
            type=str,
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'happening_on',
            type=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'),
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'location',
            type=str,
            required=True,
            location=['form', 'json']
        )

    def get(self, uuid, user):
        meetup = meetup_model.get_meet_up_by_uuid(uuid)

        if not meetup:
            return {'message': 'Meetup not found'}, 404
        return {'meetup': marshal(meetup, meetup_fields)}


meetup_api = Blueprint('resources.meetups', __name__)
api = Api(meetup_api, catch_all_404s=True)
api.add_resource(
    MeetupList,
    '',
    endpoint='meetups'
)
api.add_resource(
    Meetup,
    '/<uuid>',
    endpoint='meetup'
)
