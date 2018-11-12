import unittest
import json

from app import create_app


class TestAdmin(unittest.TestCase):

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
        """ signup function """

        signup_data = {
            "username": "kelvin123",
            "email": "kelvin@gmial.com",
            "password": "kelvin1234",
            "is_admin": 1
        }
        response = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(signup_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def login(self):
        """ login function """

        login_data = {
            "username": "kimame123",
            "password": "Kimame1234"
        }

        response = self.client.post(
            "api/v1/auth/login",
            data=json.dumps(login_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def get_token(self):
        """get token """

        self.signup()

        response = self.login()

        token = json.loads(response.data).get("token", None)
        return token

    def post_parcel(self):
        '''method to post an order'''
        token = self.get_token()

        data = {
            "origin": "nairobi",
            "price": 200,
            "destination": "kisii",
            "weight": 20
        }
        res = self.client.post(
            "/api/v1/placeorder/orders",
            data=json.dumps(data),
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'}
        )

    # def test_mark_order_as_in_transit(self):
    #     '''test for parcel orders marked intransit by admin'''

    #     res = self.client.put(
    #         "/api/v1/orders/1/intransit",

    #         headers={"content-type": "application/json"}
    #     )

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(json.loads(res.data)[
    #                      'message'], "please approve the order first")
