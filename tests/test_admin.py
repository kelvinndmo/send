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
            "username": "kimame123",
            "email": "kimame@gmial.com",
            "password": "Kimame1234",
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
            "/api/v1/parcels",
            data=json.dumps(data),
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'}
        )

    def test_update_the_status_of_an_order(self):
        """ Test update food order status """
        token = self.get_token()

        self.post_parcel()
        status_data = {
            "status": "Pending"
        }

        response = self.client.put(
            "/api/v1/parcels/1/approved",
            data=json.dumps(status_data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_complete_order(self):
        '''complete an already approved order'''
        token = self.get_token()

        self.post_parcel()
        status_data = {
            "status": "In Transit"
        }

        response = self.client.put(
            "/api/v1/parcels/1/completed",
            data=json.dumps(status_data),
            headers={"content-type": 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)[
                         'message'], "order already declined")

    def test_complete_order_non_existing(self):
        '''complete an already approved order'''
        token = self.get_token()

        self.post_parcel()
        status_data = {
            "status": "In Transit"
        }

        response = self.client.put(
            "/api/v1/orders/11111111111111111111111/completed",
            data=json.dumps(status_data),
            headers={"content-type": 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_admin_decline_order(self):
        """ Test update food order status """
        token = self.get_token()

        self.post_parcel()
        status_data = {
            "status": "Pending"
        }

        response = self.client.put(
            "/api/v1/parcels/1/declined",
            data=json.dumps(status_data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_admin_decline_order_invalid(self):
        """ Test update food order status """
        token = self.get_token()

        self.post_parcel()
        status_data = {
            "status": "Pending"
        }

        response = self.client.put(
            "/api/v1/orders/11111111111111/declined",
            data=json.dumps(status_data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_admin_mark_order_complete(self):
        """ Test update food order status """
        token = self.get_token()

        self.post_parcel()
        status_data = {
            "status": "approved"
        }

        response = self.client.put(
            "/api/v1/parcels/1/completed",
            data=json.dumps(status_data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_admin_mark_order_complete_non_exist(self):
        """ Test update food order status """
        token = self.get_token()

        self.post_parcel()
        status_data = {
            "status": "approved"
        }

        response = self.client.put(
            "/api/v1/orders/111111111111/completed",
            data=json.dumps(status_data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_admin_mark_order_complete_pending(self):
        """ Test update food order status """
        token = self.get_token()

        self.post_parcel()
        status_data = {
            "status": "pending"
        }

        response = self.client.put(
            "/api/v1/parcels/1/completed",
            data=json.dumps(status_data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def update_status_non_exisiting_order(self):
        '''update status of order not existing'''
        token = self.get_token()

        self.post_parcel()
        status_data = {
            "status": "Pending"
        }

        response = self.client.put(
            "/api/v1/orders/1111111111111111111/approved",
            data=json.dumps(status_data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'
                     }
        )

        self.assertEqual(response.status_code, 200)
