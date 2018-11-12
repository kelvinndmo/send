from flask import Flask, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Order, orders, destinations,user_orders
from utils import validators
import datetime


class PostParcel(Resource):
    '''place parcel order.'''

    @jwt_required
    def post(self):
        '''place a new parcel order.'''

        data = request.get_json()
        origin = data['origin']
        price = data['price']
        destination = data['destination']
        weight = data['weight']

        validate = validators.Validators()

        if not validate.valid_destination_name(destination):
            return {'message': "destination is invalid"}, 400

        if not validate.valid_origin_name(origin):
            return {'message': "invalid origin name"}, 400

        if type(price) != int:
            return {'message': "Invalid price"}, 400

        if type(weight) != int:
            return {'message': "Invalid weight"}, 400

        order = Order(origin, price, destination, weight)

        if order.destination in destinations:
            orders.append(order)
            return {"message": "keep tight!Your parcel order has been placed!"}, 201
        return {"message": "sorry we do not deliver to {}".format(order.destination)}


class GetOrders(Resource):

    @jwt_required
    def get(self):
        return {"orders": [order.serialize() for order in orders]}


class SpecificOrder(Resource):
    '''fetch a specific parcel order by id'''

    @jwt_required
    def get(self, id):
        '''get a specific order by id'''

        order = Order().get_by_id(id)

        if order:
            return {"order": order.serialize()}, 200

        return {"message": "Order not found"}, 404

    @jwt_required
    def delete(self, id):
        '''delete a specific order'''

        order = Order().get_by_id(id)

        if order:
            orders.remove(order)
            return {"message": "order deleted successfully"}, 200
        return {"message": "Order not found"}, 404

    @jwt_required
    def put(self, id):
        '''approve an  a parcel order'''
        order = Order().get_by_id(id)

        if order:
            if order.status != "Pending":
                return {"message": "order already {}".format(order.status)}, 200
            order.status = "approved"
            return {"message": "your parcel order has been approved"}, 200
        return {"message": "order not found"}, 404


class InTransitOrders(Resource):

    @jwt_required
    def get(self):
        return {"In Transitorder": [order.serialize() for order in orders if order.status == "In Transit"]}


class GetAcceptedOrders(Resource):

    @jwt_required
    def get(self):
        '''return list of approved orders'''

        return {
            "approved_orders": [
                order.serialize() for order in orders
                if order.status == "approved"
            ]
        }, 200


class DeclinedOrders(Resource):

    @jwt_required
    def get(self):
        '''return all orders'''

        return {
            "declined orders": [
                order.serialize() for order in orders
                if order.status == "declined"
            ]
        }


class CompletedOrders(Resource):

    @jwt_required
    def get(self):
        '''return a list of parcel orders completed by admin'''

        return {"completed orders": [
            order.serialize() for order in orders
            if order.status == "completed"
        ]
        }, 200


class SpecificUserorders(Resource):

    @jwt_required
    def get(self, id):
       return {"orders":[order.serialize() for order in orders if get_jwt_identity() == id]}

class CancelOrder(Resource):

    @jwt_required
    def put(self, id):
        '''cancel a specific order by id'''
        
        order = Order().get_by_id(id)
        if order:
            if order.status != "Pending":
                return {"message": "order already {}".format(order.status)}
            order.status == "canceled"
            return {"message":"order canceled!"},200
        return {"message":"order not found"},404

