import unittest

import json

from app import create_app


class TestUser(unittest.TestCase):

    def setUp(self):
        """ setting up testing """

        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """ Teardown """
        self.app_context.pop()

    def signup(self):
        """ signup method"""
        signup_data = {
            "username": "novak254",
            "email": "novak@gmail.com",
            "password": "Novak2544",
            "is_admin": 1
        }
        response = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(signup_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def login(self):
        """ login method """
        login_data = {
            "username": "novak254",
            "password": "Novak2544"
        }
        response = self.client.post(
            "api/v1/auth/login",
            data=json.dumps(login_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def get_token(self):
        """ get_token method """
        self.signup()
        response = self.login()
        token = json.loads(response.data).get("token", None)
        return token

    def test_login(self):
        """ Test for login """
        self.signup()
        response = self.login()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(json.loads(response.data)[
                         "message"], "successfully logged")

    def test_email_exists(self):
        """ Test signup with an existing email """
        data = {
            "username": "ndemo",
            "email": "novakkk@gmail.com",
            "password": "Novak25444"
        }
        self.signup()

        response = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(response.status_code, 201)


    def test_existing_username(self):
        """ Test singup with existing username """
        data = {
            "username": "novak254",
            "email": "novak@gmial.com",
            "password": "Movine123"
        }

        self.signup()

        response = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(json.loads(response.data)[
                         "message"], "user novak254 already exists")

    def test_non_existing_user_login(self):
        """ Test if user does not exist """
        data = {
            "username": "Novak",
            "password": "novak254"
        }

        self.signup()

        response = self.client.post(
            "api/v1/auth/login",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 404)

        self.assertEqual(json.loads(response.data)[
                         "message"], "user not found")

    def test_invalid_username(self):
        """ Test if username is inavalid """
        data = {
            "username": "*****1",
            "email": "novak@gmail.com",
            "password": "novak254"
        }

        response = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(json.loads(response.data)[
                         "message"], "username must contain"
                         " alphanumeric characters only")

    def test_invalid_email(self):
        data = {
            "username": "novak",
            "email": ".kelv",
            "password": "novak254"
        }

        response = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(json.loads(response.data)[
                         "message"], "enter valid email")

    def test_invalid_password(self):
        data = {
            "username": "iwobi",
            "email": "iwobi@gmail.com",
            "password": "@"
        }

        response = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(json.loads(response.data)[
                         "message"], "password should start with a capital"
                         " letter and include a number")