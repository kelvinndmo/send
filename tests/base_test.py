import unittest
import json

from app import create_app

from run import create,drop,create_admin


class BaseTest(unittest.TestCase):
    def setUp(self):
        """ setting up testing """

        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            drop()
            create()
            create_admin()

        self.user_signup_data = {
            "username": "kelvin",
            "email": "kelvin@gmial.com",
            "password": "Kelvin1234"
        }
        self.user_login_data = {
            "username": "kelvin",
            "password": "Kelvin1234"
        }
        self.admin_login_data = {
            "username": "AdminUser",
            "password": "Adminpass123"
        }
        self.post_parcel_data = {
            "origin": "juja",
            "destination": "keroka",
            "weight":20
        }
        self.invalid_destination_data = {
            "origin": "kisii",
            "destination": "*****123",
            "weight": 25
        }
        self.invalid_origin_name = {
            "origin": "***********1",
            "destination": "kisii",
            "weight":20 
        }

        self.incorects_pass_data = {
            "username": "kelvin",
            "password": "kevo"
        }
        self.email_already_exists_data = {
            "username": "kevooh",
            "email": "kelvin@gmial.com",
            "password": "kelvin1234"
        }
        self.existing_usernme_data = {
            "username": "kelvin",
            "email": "kwemoi@gmial.com",
            "password": "Kwemoi12"
        }
        self.invalid_password_data = {
            "username": "mwanzia",
            "email": "ndemo@gmail.com",
            "password": "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        }

        self.invalid_email_data = {
            "username": "novakkk",
            "email": "davis",
            "password": "kelvin123",
            "is_admin": 1
        }
        self.invalid_username_data = {
            "username": "*****1",
            "email": "kelvin@gmail.com",
            "password": "kelvin123",
            "is_admin": 1
        }
        self.user_doest_not_exist_data = {
            "username": "onkundidndem`",
            "password": "Novak254"
        } 

   
    def signup(self):
        """ user signup function """
        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(self.user_signup_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def login(self):
        """ login function """
        response = self.client.post(
            "api/v2/auth/login",
            data=json.dumps(self.user_login_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def login_admin(self):
        """ method to login admin """
        response = self.client.post(
            "api/v2/auth/login",
            data=json.dumps(self.admin_login_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def get_token_as_user(self):
        """get token """
        self.signup()
        response = self.login()
        token = json.loads(response.data).get("token", None)
        return token

    def get_token_as_admin(self):
        """get token """
        response = self.login_admin()
        token = json.loads(response.data).get("token", None)
        return token

    def complete_order(self):
        """ complete an order """

        token = self.get_token_as_admin()

        res = self.client.put(
            "api/v2/parcels/1/completed",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        return res

    def accept_order(self):
        """ accept an order """
        token = self.get_token_as_admin()

        res = self.client.put(
            "api/v2/parcels/1/approved",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        return res
    
    def mark_in_transit_order(self):
        """ accept an order """
        token = self.get_token_as_admin()

        res = self.client.put(
            "/api/v2/parcels/1/intransit",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        return res
    
    

    def reject_order(self):
        """ reject an order """
        token = self.get_token_as_admin()

        res = self.client.put(
            "api/v2/parcels/1/declined",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        return res

    def cancel_order(self):
        "cancel an order"

        token = self.get_token_as_user()

        res = self.client.put(
            "api/v2/parcels/1/cancel",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        return res

    def update_destination(self):
        '''update destination'''

        token = self.get_token_as_user()

        
        res = self.client.put(
            "api/v2/parcels/1/destination",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        
        return res


    def post_parcel(self):
        """ method to post new parcel """

        token = self.get_token_as_user()

        res = self.client.post(
            "/api/v2/parcels",
            data=json.dumps(self.post_parcel_data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        return res