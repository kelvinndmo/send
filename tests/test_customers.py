import unittest
import json

from .base_test import BaseTest


class TestPostParcel(BaseTest):

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
        """ Test parcel order does not exist """
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
        print(response)

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
    def test_get_all_order(self):
        """test for returning all orders"""

        token = self.get_token_as_user()

        self.post_parcel()

        response = self.client.get(
            "api/v2/parcels",
             headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)
    
    def test_get_one_order(self):
        """test for get one one order"""

        token = self.get_token_as_user()

        self.post_parcel()

        response = self.client.get(
            "api/v2/parcels/1",
             headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)
    
    def test_get_one_order_non_exist(self):
        """tes for orders non exsitent orders"""

        token = self.get_token_as_user()

        self.post_parcel()

        response = self.client.get(
            "api/v2/parcels/100000",
             headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)
    
    def test_get_intransit_orders(self):
        """test for returning all orders"""

        token = self.get_token_as_user()

        self.post_parcel()
        self.accept_order()
        self.mark_in_transit_order()

        response = self.client.get(
            "api/v2/parcels/intransit",
             headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_get_declined_orders(self):
        """test for returning all declined orders"""

        token = self.get_token_as_user()

        self.post_parcel()
        self.reject_order()

        response = self.client.get(
            "api/v2/parcels/declined",
             headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)
    
    def test_get_no_declined_orders(self):
        """test for returning no declined  orders"""

        token = self.get_token_as_user()

        self.post_parcel()

        response = self.client.get(
            "api/v2/parcels/declined",
             headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)
    
    def test_get_completed_orders(self):
        """test for returning all orders"""

        token = self.get_token_as_user()

        self.post_parcel()
        self.accept_order()
        self.mark_in_transit_order()
        self.complete_order()

        response = self.client.get(
            "api/v2/parcels/completedorders",
             headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)
    
    def test_get_no_completed_orders(self):
        """test for returning all orders"""

        token = self.get_token_as_user()

        self.post_parcel()
        self.accept_order()
        self.mark_in_transit_order()

        response = self.client.get(
            "api/v2/parcels/completedorders",
             headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)


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
    
    def test_cancel_order(self):
        '''test for user cancelling an order'''

        token = self.get_token_as_user()

        self.post_parcel()
        
        res = self.client.put(
            "api/v2/parcels/1/cancel",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(res.status_code, 200)
    
    def test_cancel_order(self):
        '''test for user cancelling an order'''

        token = self.get_token_as_user()

        self.post_parcel()
        self.cancel_order()
        
        res = self.client.put(
            "api/v2/parcels/1/cancel",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(res.status_code, 400)
        


    def test_mark_parcel_in_transit(self):
        token = self.get_token_as_admin()

        self.post_parcel()
        self.accept_order()

        response = self.mark_in_transit_order()

        self.assertEqual(response.status_code, 200)

    def test_mark_in_transit_order_non_existing(self):

        token = self.get_token_as_admin()

        self.post_parcel()
        self.accept_order()

        res = self.client.put(
            "/api/v2/parcels/100000000000/intransit",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'})
        
        self.assertEqual(res.status_code, 404)

    


    def test_mark_parcel_in_transit_unapproved(self):
        token = self.get_token_as_admin()

       
        self.post_parcel()
        response = self.mark_in_transit_order()

        self.assertEqual(response.status_code, 400)
    
    def test_mark_parcel_in_transit_already_completed(self):
        token = self.get_token_as_admin()

       
        self.post_parcel()
        self.accept_order()
        self.mark_in_transit_order()
        response = self.mark_in_transit_order()

        self.assertEqual(response.status_code, 400)

   

    def test_rejected_parcel_orders_does_not_exist(self):
        """ test rejected declined orders does not exist """

        token = self.get_token_as_admin()

        response = self.client.get(
            "api/v2/parcels/declined",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_complete_order(self):
        token = self.get_token_as_admin()

        self.post_parcel()
        self.accept_order()
        self.mark_in_transit_order()

        response = self.complete_order()

        self.assertEqual(response.status_code, 200)
        
    def test_complete_order_status_pending(self):
        token = self.get_token_as_admin()

        self.post_parcel()

        response = self.complete_order()

        self.assertEqual(response.status_code, 400)
        
    def test_complete_order_status_acccepted(self):
        token = self.get_token_as_admin()

        self.post_parcel()
        self.accept_order()

        response = self.complete_order()
        print(response.data)

        self.assertEqual(response.status_code, 400)
    
    def test_complete_order_rejected(self):
        token = self.get_token_as_admin()

        self.post_parcel()
        self.reject_order()

        response = self.complete_order()

        self.assertEqual(response.status_code, 400)
        
    
    def test_complete_order_already_completed(self):
        token = self.get_token_as_admin()

        self.post_parcel()
        self.accept_order()
        self.mark_in_transit_order()
        self.complete_order()

        response = self.complete_order()

        self.assertEqual(response.status_code,400)

    def test_get_specific_user_orders(self):

        token = self.get_token_as_user()
        self.post_parcel()
        response = self.client.get(
            "/api/v2/users/2/parcels",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_specific_user_orders_user_not_existing(self):

        token = self.get_token_as_admin()

        response = self.client.get(
            "/api/v2/users/1000000/parcels",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 404)