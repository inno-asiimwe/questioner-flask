from flask_testing import TestCase
from app import db, create_app


class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app('testing')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
