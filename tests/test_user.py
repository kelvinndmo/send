import unittest
import json

from .base_test import BaseTest


class TestUser(BaseTest):

    def test_signup(self):
        """ Test for signup sucessfull """
        response = self.signup()

        self.assertEqual(response.status_code, 201)

    def test_login(self):
        """ Test for login sucessfull """
        self.signup()
        response = self.login()

        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_login_as_admin(self):
        """ Test to login in admin """

        response = self.login_admin()

        self.assertEqual(response.status_code, 200)

    def test_incorect_password(self):
        """ test for incorect password """
        self.signup()
        response = self.client.post(
            "api/v2/auth/login",
            data=json.dumps(self.incorects_pass_data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 400)

    def test_email_exists(self):
        """ Test signup with an existing email """

        self.signup()

        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(self.email_already_exists_data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 400)

    def test_existing_username(self):
        """ Test singup with existing username """
        self.signup()
        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(self.existing_usernme_data),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(response.status_code, 400)

    def test_non_existing_user_login(self):
        """ Test if user does not exist """
        self.signup()

        response = self.client.post(
            "api/v2/auth/login",
            data=json.dumps(self.user_doest_not_exist_data),
            headers={'content-type': 'application/json'}
        )
        print(response.data)
        self.assertEqual(response.status_code, 404)

        self.assertEqual(json.loads(response.data)[
                         "message"], "user not found")

    def test_invalid_username(self):
        """ Test if username is invalid """

        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(self.invalid_username_data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_email(self):
        """ Test invalid email """
        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(self.invalid_email_data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(json.loads(response.data)[
                         "message"], "invalid email adress")

    def test_invalid_password(self):
        """ Test invalid password """
        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(self.invalid_password_data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 400)