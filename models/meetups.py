import datetime
import uuid
from flask import current_app
from app import db
from .user import User


class Meetup(db.Model):
    __tablename__ = 'meetups'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(256), default=str(uuid.uuid4()))
    created_by = db.Column(
        db.Integer, db.ForeignKey(User.id, ondelete='cascade'), nullable=False
        )
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    location = db.Column(db.String(256), nullable=False)
    topic = db.Column(db.Text, nullable=False)
    happening_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, topic, happening_on, location, created_by):
        self.uuid = uuid.uuid4()
        self.topic = topic
        self.happening_on = happening_on
        self.location = location
        self.created_by = created_by

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_meetups(cls):
        return cls.query.all()

    @classmethod
    def meetup_exists(cls, topic, location, happening_on):
        return cls.query.filter_by(
            topic=topic
        ).filter_by(
            location=location
        ).filter_by(
            happening_on=happening_on
        ).first()

    @classmethod
    def get_meet_up_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def __repr__(self):
        return '<Meetup: {}>'.format(self.topic)
