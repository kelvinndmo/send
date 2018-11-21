from flask import Flask, request
from functools import wraps
from flask_restful import Resource
from models.models import User, Parcel

from utils import validators
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

def admin_access(f):
    ''' Restrict access if not admin '''
    @wraps(f)
    def wrapper_function(*args, **kwargs):
        user = User().get_by_username(get_jwt_identity())
        if  user.username !="AdminUser":
            return {'message': 'Your cannot access this level'}, 401
        return f(*args, **kwargs)

    return wrapper_function


class AcceptStatus(Resource):
    
    @jwt_required
    @admin_access
    def put(self, id):
        '''mark an order as approved by admin'''

        order = Parcel().get_by_id(id)

        if order:
            if order.status != "Pending":
                return {"message": "order already {}".format(order.status)}, 200
            order.accept_status(id)
            return {"message": "your order has been approved"}, 200
        return {"message": "order not found"}, 404
        
class CompleteOrder(Resource):
    
    @jwt_required
    @admin_access
    def put(self, id):
        '''mark an order as completed by admin'''
        order = Parcel().get_by_id(id)

        if order:
            if order.status == "completed" or order.status == "declined":
                return {"message": "order already {}".format(order.status)}

            if order.status == "Pending":
                return {"message": "please approve the order first "}

            if order.status == "In Transit":
                order.complete_accepted_order(id)
                return {
                    "message":
                    "Your has been order completed awaiting delivery"
                }

        return {"message": "Order not found"}, 404


class MarkOrderInTransit(Resource):
    
    @jwt_required
    @admin_access
    def put(self, id):
        '''mark order has started being transported'''
        order = Parcel().get_by_id(id)

        if order:
            if order.status == "In Transit":
                return {"message":"Order already in Transit"},400
            if order.status == "completed" or order.status == "declined":
                return {"You have already marked the order as {}".format(order.status)}, 200

            if order.status == "Pending":
                return {"message": "please approve the order first"}, 200

            if order.status == "accepted":
                order.mark_in_transit(id)
                return {"message": "The order is now on the road!Rember to keep track of the order"}, 200

        return {"message": "The order could not be found!,check on the id please"}, 404


class DeclineOrder(Resource):

    @jwt_required
    @admin_access
    def put(self, id):
        '''decline a specific order'''

        order = Parcel().get_by_id(id)

        if order:

            if order.status != "Pending":
                return {"message": "order already {}".format(order.status)}

            order.decline_order(id)
            return {"message": "Order declined"}

        return {"message": "Order not found"}, 404

class UpdateLocation(Resource):

    @jwt_required
    @admin_access
    def put(self, id):

        data = request.get_json()
        current_location = data['current_location']

        parcel = Parcel().get_by_id(id)

        if parcel:
            parcel.current_location = current_location
            parcel.update_location(id)

            return {'parcel': parcel.serialize()}, 200
        return {'message':'parcel does not exist'}, 404
