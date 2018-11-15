import unittest
import json

from app import create_app


class TestFoodOrder(unittest.TestCase):

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
            "password": "Kelvin1234",
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
            "username": "kelvin123",
            "password": "Kelvin1234"
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

    def test_place_parcel_order(self):
        '''test for invalid destination'''

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
        print(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json.loads(res.data)[
                         'message'], "keep tight!Your parcel order has been placed!")

    def test_place_parcel_order_invalid_dest(self):
        '''test for placing a parcel order invalid destination'''

        token = self.get_token()

        data = {
            "origin": "nairobi",
            "price": 200,
            "destination": "**********",
            "weight": 20
        }

        res = self.client.post(
            "/api/v1/parcels",
            data=json.dumps(data),
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'}
        )
        print(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "destination is invalid")

        def test_place_parcel_order_invalid_origin(self):
            '''test for placing a parcel order invalid origin'''

        token = self.get_token()

        data = {
            "origin": "nairobi****",
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

        def test_place_parcel_order_invalid_price(self):
            '''test for placing a parcel order invalid price'''

        token = self.get_token()

        data = {
            "origin": "nairobi",
            "price": "**",
            "destination": "kisii",
            "weight": 20
        }

        res = self.client.post(
            "/api/v1/parcels",
            data=json.dumps(data),
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'}
        )
        print(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Invalid price")

        def test_place_parcel_order_invalid_price(self):
            '''test for placing a parcel order invalid price'''

        token = self.get_token()

        data = {
            "origin": "nairobi",
            "price": 30,
            "destination": "kisii",
            "weight": "we"
        }

        res = self.client.post(
            "/api/v1/parcels",
            data=json.dumps(data),
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'}
        )
        print(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Invalid weight")

    def test_get_all_orders(self):
        '''get all placed orders'''

        token = self.get_token()

        res = self.client.get(
            "/api/v1/parcels",
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'}
        )
        print(res.data)
        self.assertEqual(res.status_code, 200)

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
        return res

    def test_order_by_id(self):
        '''get parcel order by id'''

        token = self.get_token()
        self.post_parcel()

        res = self.client.get(
            "/api/v1/parcels/1",
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'}
        )

        print(res.data)
        self.assertEqual(res.status_code, 200)

    def test_get_accepted_orders(self):
        '''test for getting a list of all orders accepted by admin'''
        token = self.get_token()

        res = self.client.get(
            "/api/v1/acceptedorders",
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(res.status_code, 200)

    def accept_order(self):
        """ accept an order """
        token = self.get_token()

        res = self.client.put(
            "api/v1/orders/1/approved",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        return res

    def cancel_order(self):
        """ cancel an order """
        token = self.get_token()

        res = self.client.put(
            "/parcels/1/cancel",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        return res

    def test_completed_orders(self):
        '''test for returning a list of completed orders'''

        token = self.get_token()

        res = self.client.get(
            "/api/v1/parcels/completedorders",
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(res.status_code, 200)

    def test_non_order_by_id(self):
        '''testing for a an order that doesn't exist'''
        token = self.get_token()

        res = self.client.get(
            "/api/v1/parcels/111",
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "order of id 111 not found")

    def test_get_orders_in_transit(self):

        token = self.get_token()

        res = self.client.get(
            "/api/v1/parcels/intransit",
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'})
        self.assertEqual(res.status_code, 200)

    def test_cancel_parcel_order(self):
        """test for cancelling a specific order"""
        token = self.get_token()
        self.post_parcel()

        res = self.cancel_order()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Order canceled")