# import unittest
# import json
# from app import create_app


# class TestOrders(unittest.TestCase):
#     def setUp(self):
#         '''set the app for testing
#         setting a test client for testing'''

#         self.app = create_app("testing")
#         self.client = self.app.test_client()
#         self.app_context = self.app.app_context()
#         self.app_context.push()

#     def tearDown(self):

#         self.app_context.pop()

#     def test_create_parcel_order(self):
#         '''test place a parcel order'''
#         data = {
#             "origin": "nairobi",
#             "price": 200,
#             "destination": "kisii",
#             "weight": 20
#         }

#         res = self.client.post(
#             "/api/v1/placeorder/orders",
#             data=json.dumps(data),
#             headers={"content-type": "application/json"}
#         )

#         self.assertEqual(res.status_code, 201)
#         self.assertEqual(json.loads(res.data)[
#                          'message'], "keep tight!Your parcel order has been placed!")

#     def test_get_all_orders(self):
#         '''get all placed orders'''

#         res = self.client.get(
#             "/api/v1/orders",
#             headers={"content-type": "application/json"}
#         )
#         print(res.data)
#         self.assertEqual(res.status_code, 200)

#     def test_order_by_id(self):
#         '''get parcel order by id'''

#         res = self.client.get(
#             "/api/v1/orders/1",
#             headers={"content-type": "application/json"}
#         )

#         print(res.data)
#         self.assertEqual(res.status_code, 200)
    
#     def test_update_status_approved(self):
#         '''test for a parcel order whose status has been approved'''

#         res = self.client.put(
#             "/api/v1/orders/1/approved",
#             headers={"content-type": "application/json"}
#         )

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(json.loads(res.data)[
#                          'message'], "your order has been approved")

#     def test_mark_order_as_completed(self):
#         '''test for parcel orders completed by admin'''

#         res = self.client.put(
#             "/api/v1/orders/1/completed",

#             headers={"content-type": "application/json"}
#         )

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(json.loads(res.data)[
#                          'message'], "please approve the order first ")

#     def test_declined_orders_by_admin(self):
#         '''test for returning a list of parcel orders declined by admin'''

#         res = self.client.get(
#             "/api/v1/orders/declined",
#             headers={"content-type": "application/json"}
#         )
#         self.assertEqual(res.status_code, 200)

#     def post_parcel(self):
#         '''method to post an order'''
#         data = {
#             "origin": "kiambu",
#             "price": 20,
#             "destination": "juja",
#             "weight": 25
#         }
#         res = self.client.post(
#             "/api/v1/placeorder/orders",
#             data=json.dumps(data),
#             headers={"content-type": "application/json"}
#         )
#         return res

#     def test_get_accepted_orders(self):
#         '''test for getting a list of all orders accepted by admin'''

#         res = self.client.get(
#             "/api/v1/acceptedorders",
#             headers={"content-type": "application/json"}
#         )
#         self.assertEqual(res.status_code, 200)



#     def test_completed_orders(self):
#         '''test for returning a list of completed orders'''

#         res = self.client.get(
#             "/api/v1/orders/completedorders",
#             headers={"content-type": "application/json"}
#         )
#         self.assertEqual(res.status_code, 200)

#     def test_non_order_by_id(self):
#         '''testing for a an order that doesn't exist'''

#         res = self.client.get(
#             "/api/v1/orders/111",
#             headers={"content-type": "application/json"}
#         )
#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(json.loads(res.data)[
#                          'message'], "Order not found")

#     def test_non_order_delete(self):
#         '''deleting an order that doesn't exist'''

#         res = self.client.delete(
#             "api/v1/orders/1111111111",
#             headers={"content-type": "application/json"}
#         )
#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(json.loads(res.data)[
#                          'message'], "Order not found")

#     def test_declined_orders_list(self):
#         '''testing for declined order'''

#         res = self.client.get(
#             "/api/v1/orders/declined",
#             headers={"content-type": "application/json"}
#         )
#         self.assertEqual(res.status_code, 200)
        

#     def test_mark_order_as_in_transit(self):
#         '''test for parcel orders marked intransit by admin'''

#         res = self.client.put(
#             "/api/v1/orders/1/intransit",

#             headers={"content-type": "application/json"}
#         )

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(json.loads(res.data)[
#                          'message'], "please approve the order first")

#     def test_get_orders_in_transit(self):
#         res = self.client.get(
#             "/api/v1/orders/intransit",
#             headers={"content-type": "application/json"})
#         self.assertEqual(res.status_code, 200)

#     def test_invalid_origin_name(self):
#         '''test for invalid food name'''
#         data = {
#             "origin": "******",
#             "price": 20,
#             "destination": "kiambu",
#             "weight": 5
#         }

#         res = self.client.post(
#             "/api/v1/placeorder/orders",
#             data=json.dumps(data),
#             headers={"content-type": "application/json"}
#         )

#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(json.loads(res.data)[
#                          'message'], "invalid origin name")

#     def test_invalid_destination(self):
#         '''test for invalid destination'''
#         data = {
#             "origin": "kiambu",
#             "price": 20,
#             "destination": "!!!!!!!",
#             "weight": 5
#         }

#         res = self.client.post(
#             "/api/v1/placeorder/orders",
#             data=json.dumps(data),
#             headers={"content-type": "application/json"}
#         )

#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(json.loads(res.data)[
#                          'message'], "destination is invalid")

#     def test_invalid_price(self):
#         '''test for invalid  price'''
#         data = {
#             "origin": "kiambu",
#             "price": "kevo",
#             "destination": "kiambu",
#             "weight": 5
#         }

#         res = self.client.post(
#             "/api/v1/placeorder/orders",
#             data=json.dumps(data),
#             headers={"content-type": "application/json"}
#         )

#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(json.loads(res.data)['message'], "Invalid price")

#     def test_invalid_weight(self):
#         '''test for invalid  price'''
#         data = {
#             "origin": "kiambu",
#             "price": 50,
#             "destination": "kiambu",
#             "weight": "kevo"
#         }

#         res = self.client.post(
#             "/api/v1/placeorder/orders",
#             data=json.dumps(data),
#             headers={"content-type": "application/json"}
#         )

#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(json.loads(res.data)['message'], "Invalid weight")

#     # def test_delete_order(self):
#     #     '''test for deleting an order'''

   
#     #     res = self.client.delete(
#     #         "/api/v1/orders/1",
#     #         headers={"content-type": "application/json"}

#     #     )
#     #     self.assertEqual(res.status_code, 200)

#     # def test_complete_non_existing_order(self):
#     #     '''test when you try to complete an order that does not exist'''

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
            "username": "kimame123",
            "email": "kimame@gmail.com",
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
        """ login method """
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
        """ get_token method """
        self.signup()
        response = self.login()
        token = json.loads(response.data).get("token", None)
        return token

    # def test_signup(self):
    #     """ Test for signup """
    #     response = self.signup()
    #     self.assertEqual(response.status_code, 201)

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
            "username": "daviskk",
            "email": "kimame@gmail.com",
            "password": "Kwemoi12",
            "is_admin": 1
        }
        self.signup()

        response = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(response.status_code, 400)

        self.assertEqual(json.loads(response.data)[
                         "message"], "user with kimame@gmail.com"
                         " already exists")

    def test_existing_username(self):
        """ Test singup with existing username """
        data = {
            "username": "kimame123",
            "email": "kwemoi@gmial.com",
            "password": "Kwemoi12",
            "is_admin": 1
        }

        self.signup()

        response = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(json.loads(response.data)[
                         "message"], "user kimame123 already exists")

    def test_non_existing_user_login(self):
        """ Test if user does not exist """
        data = {
            "username": "kimame",
            "password": "Kimame123"
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
            "email": "davis@gmail.com",
            "password": "kimame123",
            "is_admin": 1
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
            "username": "daviskk",
            "email": "davis",
            "password": "kimame123",
            "is_admin": 1
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
            "username": "mwanzia",
            "email": "mwanzia@gmail.com",
            "password": "aimame123",
            "is_admin": 1
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
