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

    def test_place_parcel_order(self):
        '''test for placing a parcel order'''

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
        print(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json.loads(res.data)[
                         'message'], "keep tight!Your parcel order has been placed!")

    def test_get_all_orders(self):
        '''get all placed orders'''

        token = self.get_token()

        res = self.client.get(
            "/api/v1/orders",
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
            "/api/v1/placeorder/orders",
            data=json.dumps(data),
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'}
        )
        return res

    # def test_order_by_id(self):
    #     '''get parcel order by id'''

    #     token = self.get_token()
    #     self.post_parcel()

    #     res = self.client.get(
    #         "/api/v1/orders/1",
    #         headers={"content-type": "application/json",
    #                  'Authorization': f'Bearer {token}'}
    #     )

    #     print(res.data)
    #     self.assertEqual(res.status_code, 200)

    def test_declined_orders_by_admin(self):
        '''test for returning a list of parcel orders declined by admin'''
        token = self.get_token()

        res = self.client.get(
            "/api/v1/orders/declined",
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'}
        )
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

    def test_completed_orders(self):
        '''test for returning a list of completed orders'''

        token = self.get_token()

        res = self.client.get(
            "/api/v1/orders/completedorders",
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(res.status_code, 200)

    def test_non_order_by_id(self):
        '''testing for a an order that doesn't exist'''
        token = self.get_token()

        res = self.client.get(
            "/api/v1/orders/111",
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Order not found")

    def test_declined_orders_list(self):
        '''testing for declined order'''
        token = self.get_token()

        res = self.client.get(
            "/api/v1/orders/declined",
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'
                     }
        )
        self.assertEqual(res.status_code, 200)

    def test_get_orders_in_transit(self):

        token = self.get_token()

        res = self.client.get(
            "/api/v1/orders/intransit",
            headers={"content-type": "application/json",
                     'Authorization': f'Bearer {token}'})
        self.assertEqual(res.status_code, 200)
