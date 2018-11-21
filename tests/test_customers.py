import unittest
import json

from .base_test import BaseTest


class TestFoodOrder(BaseTest):

    def test_post_parcel(self):
        ''' test for  posting a parcel'''
        response = self.post_parcel()

        self.assertEqual(response.status_code, 201)
        
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
        self.assertEqual(json.loads(response.data)[
                          'message'], "your order has been approved")
    
    
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

        token = self.get_token_as_admin()

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

 