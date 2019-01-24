import json
from .base import BaseTestCase


class TestUser(BaseTestCase):

    def test_successful_registration(self):
        with self.client:
            response = self.client.post(
                '/api/v1/users/register',
                data=json.dumps(
                    dict(
                        email="asiimwe@asiimwe.com",
                        password="password"
                    )
                ),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('asiimwe@asiimwe.com', data['user']['email'])
            self.assertIn('uuid', data['user'])

    def test_duplicate_registration(self):
        with self.client:
            response = self.client.post(
                '/api/v1/users/register',
                data=json.dumps(
                    dict(
                        email="asiimwe@asiimwe.com",
                        password="password"
                    )
                ),
                content_type='application/json'
            )
            duplicate_response = self.client.post(
                '/api/v1/users/register',
                data=json.dumps(
                    dict(
                        email="asiimwe@asiimwe.com",
                        password="password2345"
                    )
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            duplicate_data = json.loads(duplicate_response.data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(duplicate_response.status_code, 409)
            self.assertIn(
                "email already registered",
                duplicate_data['message']
                )

    def test_successful_login(self):
        with self.client:
            register_response = self.client.post(
                '/api/v1/users/register',
                data=json.dumps(
                    dict(
                        email='asiimwe@asiimwe.com',
                        password='password'
                    )
                ),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/users/login',
                data=json.dumps(
                    dict(
                        email='asiimwe@asiimwe.com',
                        password='password'
                    )
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('token', data)

    def test_failed_login(self):
        with self.client:
            register_response = self.client.post(
                '/api/v1/users/register',
                data=json.dumps(
                    dict(
                        email='asiimwe@asiimwe.com',
                        password='password'
                    )
                ),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/users/login',
                data=json.dumps(
                    dict(
                        email='asiimwe@outlook.com',
                        password='password'
                    )
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn('Login failed', data['message'])
