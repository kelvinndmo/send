import unittest
import json

from .base_test import BaseTest


class TestFoodOrder(BaseTest):

    def test_invalid_destination(self):
        """ Test for an invalid destination """

        token = self.get_token_as_user()
        response = self.client.post(
            "/api/v2/parcels",
            data=json.dumps(self.invalid_destination_data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 400)

    def test_get_parcel_order_does_not_exist(self):
        """ Test food order does not exist """
        token = self.get_token_as_user()

        response = self.client.get(
            "api/v2/parcels/100",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_accept_order(self):
        """ test to accept order """

        token = self.get_token_as_admin()

        self.post_parcel()

        response = self.accept_order()

        self.assertEqual(response.status_code, 200)
    
    
    def test_get_all_accepted_parcel_order(self):
        """ test get all accept parcel orders """

        token = self.get_token_as_admin()

        self.post_parcel()

        self.accept_order()

        response = self.client.get(
            "api/v2/parcels/acceptedorders",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)
    
    def test_accepted_parcel_order_does_not_exist(self):
        """ test accepted parcel orders does not exist """

        token = self.get_token_as_admin()

        response = self.client.get(
            "api/v2/parcel/acceptedorders",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)
    
    def test_reject_order(self):
        """ test to accept order """

        token = self.get_token_as_user()

        self.post_parcel()

        response = self.client.put(
            "api/v2/parcels/1/declined",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)


    def test_rejected_parcel_orders_does_not_exist(self):
        """ test rejected declined orders does not exist """

        token = self.get_token_as_admin()

        response = self.client.get(
            "api/v2/parcels/declined",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)























# import unittest
# import json

# from app import create_app


# class TestFoodOrder(unittest.TestCase):

#     def setUp(self):
#         """ setting up testing """

#         self.app = create_app('testing')
#         self.client = self.app.test_client()
#         self.app_context = self.app.app_context()
#         self.app_context.push()

#     def tearDown(self):
#         """ Teardown """
#         self.app_context.pop()

#     def signup(self):
#         """ signup function """

#         signup_data = {
#             "username": "kelvin123",
#             "email": "kelvin@gmial.com",
#             "password": "Kelvin1234",
#             "is_admin": 1
#         }
#         response = self.client.post(
#             "api/v2/auth/signup",
#             data=json.dumps(signup_data),
#             headers={'content-type': 'application/json'}
#         )
#         return response

#     def login(self):
#         """ login function """

#         login_data = {
#             "username": "kelvin123",
#             "password": "Kelvin1234"
#         }

#         response = self.client.post(
#             "api/v2/auth/login",
#             data=json.dumps(login_data),
#             headers={'content-type': 'application/json'}
#         )
#         return response

#     def get_token(self):
#         """get token """

#         self.signup()

#         response = self.login()

#         token = json.loads(response.data).get("token", None)
#         return token

#     def test_place_parcel_order(self):
#         '''test for invalid destination'''

#         token = self.get_token()

#         data = {
#             "origin": "nairobi",
#             "price": 200,
#             "destination": "kisii",
#             "weight": 20
#         }

#         res = self.client.post(
#             "/api/v2/parcels",
#             data=json.dumps(data),
#             headers={"content-type": "application/json",
#                      'Authorization': f'Bearer {token}'}
#         )
#         self.assertEqual(res.status_code, 201)
#         self.assertEqual(json.loads(res.data)[
#                          'message'], "keep tight!Your parcel order has been placed!")

    # def test_place_parcel_order_invalid_dest(self):
    #     '''test for placing a parcel order invalid destination'''

    #     token = self.get_token()

    #     data = {
    #         "origin": "nairobi",
    #         "price": 200,
    #         "destination": "**********",
    #         "weight": 20
    #     }

    #     res = self.client.post(
    #         "/api/v2/parcels",
    #         data=json.dumps(data),
    #         headers={"content-type": "application/json",
    #                  'Authorization': f'Bearer {token}'}
    #     )
    #     print(res.data)
    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(json.loads(res.data)[
    #                      'message'], "destination is invalid")

    #     def test_place_parcel_order_invalid_origin(self):
    #         '''test for placing a parcel order invalid origin'''

    #     token = self.get_token()

    #     data = {
    #         "origin": "nairobi****",
    #         "price": 200,
    #         "destination": "kisii",
    #         "weight": 20
    #     }

    #     res = self.client.post(
    #         "/api/v2/parcels",
    #         data=json.dumps(data),
    #         headers={"content-type": "application/json",
    #                  'Authorization': f'Bearer {token}'}
    #     )

    #     def test_place_parcel_order_invalid_price(self):
    #         '''test for placing a parcel order invalid price'''

    #     token = self.get_token()

    #     data = {
    #         "origin": "nairobi",
    #         "price": "**",
    #         "destination": "kisii",
    #         "weight": 20
    #     }

    #     res = self.client.post(
    #         "/api/v2/parcels",
    #         data=json.dumps(data),
    #         headers={"content-type": "application/json",
    #                  'Authorization': f'Bearer {token}'}
    #     )
    #     print(res.data)
    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(json.loads(res.data)[
    #                      'message'], "Invalid price")

    #     def test_place_parcel_order_invalid_price(self):
    #         '''test for placing a parcel order invalid price'''

    #     token = self.get_token()

    #     data = {
    #         "origin": "nairobi",
    #         "price": 30,
    #         "destination": "kisii",
    #         "weight": "we"
    #     }

    #     res = self.client.post(
    #         "/api/v2/parcels",
    #         data=json.dumps(data),
    #         headers={"content-type": "application/json",
    #                  'Authorization': f'Bearer {token}'}
    #     )
    #     print(res.data)
    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(json.loads(res.data)[
    #                      'message'], "Invalid weight")

    # def test_get_all_orders(self):
    #     '''get all placed orders'''

    #     token = self.get_token()

    #     res = self.client.get(
    #         "/api/v2/parcels",
    #         headers={"content-type": "application/json",
    #                  'Authorization': f'Bearer {token}'}
    #     )
    #     print(res.data)
    #     self.assertEqual(res.status_code, 200)

    # def post_parcel(self):
    #     '''method to post an order'''
    #     token = self.get_token()

    #     data = {
    #         "origin": "nairobi",
    #         "price": 200,
    #         "destination": "kisii",
    #         "weight": 20
    #     }
    #     res = self.client.post(
    #         "/api/v2/parcels",
    #         data=json.dumps(data),
    #         headers={"content-type": "application/json",
    #                  'Authorization': f'Bearer {token}'}
    #     )
    #     return res

    # def test_order_by_id(self):
    #     '''get parcel order by id'''

    #     token = self.get_token()
    #     self.post_parcel()

    #     res = self.client.get(
    #         "/api/v2/parcels/1",
    #         headers={"content-type": "application/json",
    #                  'Authorization': f'Bearer {token}'}
    #     )

    #     print(res.data)
    #     self.assertEqual(res.status_code, 200)

    # def test_get_accepted_orders(self):
    #     '''test for getting a list of all orders accepted by admin'''
    #     token = self.get_token()

    #     res = self.client.get(
    #         "/api/v2/acceptedorders",
    #         headers={"content-type": "application/json",
    #                  'Authorization': f'Bearer {token}'}
    #     )
    #     self.assertEqual(res.status_code, 200)

    # def accept_order(self):
    #     """ accept an order """
    #     token = self.get_token()

    #     res = self.client.put(
    #         "api/v2/orders/1/approved",
    #         headers={'content-type': 'application/json',
    #                  'Authorization': f'Bearer {token}'}
    #     )
    #     return res

    # def cancel_order(self):
    #     """ cancel an order """
    #     token = self.get_token()

    #     res = self.client.put(
    #         "/api/v2/parcels/1/cancel",
    #         headers={'content-type': 'application/json',
    #                  'Authorization': f'Bearer {token}'}
    #     )
    #     return res

    # def test_completed_orders(self):
    #     '''test for returning a list of completed orders'''

    #     token = self.get_token()

    #     res = self.client.get(
    #         "/api/v2/parcels/completedorders",
    #         headers={"content-type": "application/json",
    #                  'Authorization': f'Bearer {token}'}
    #     )
    #     self.assertEqual(res.status_code, 200)

    # def test_non_order_by_id(self):
    #     '''testing for a an order that doesn't exist'''
    #     token = self.get_token()

    #     res = self.client.get(
    #         "/api/v2/parcels/111",
    #         headers={"content-type": "application/json",
    #                  'Authorization': f'Bearer {token}'}
    #     )
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(json.loads(res.data)[
    #                      'message'], "order of id 111 not found")

    # def test_get_orders_in_transit(self):

    #     token = self.get_token()

    #     res = self.client.get(
    #         "/api/v2/parcels/intransit",
    #         headers={"content-type": "application/json",
    #                  'Authorization': f'Bearer {token}'})
    #     self.assertEqual(res.status_code, 200)

    # def test_cancel_parcel_order(self):
    #     """test for cancelling a specific order"""
    #     token = self.get_token()
    #     self.post_parcel()

    #     res = self.cancel_order()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(json.loads(res.data)[
    #                      'message'], "Order canceled")
