from flask import Flask, request
from flask_restful import Resource
from models.models import Order, orders, destinations
from utils import validators
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime



class AcceptStatus(Resource):

    @jwt_required
    def put(self, id):
        '''mark an order as approved'''

        order = Order().get_by_id(id)

        if order:
            if order.status != "Pending":
                return {"message": "order already {}".format(order.status)}, 200
            order.status = "approved"
            return {"message": "your order has been approved"}, 200

        return {"message": "order not found"}, 404


class CompleteOrder(Resource):

    @jwt_required
    def put(self, id):
        '''mark an order as completed by admin'''
        order = Order().get_by_id(id)

        if order:
            if order.status == "completed" or order.status == "declined":
                return {"message": "order already {}".format(order.status)}

            if order.status == "Pending":
                return {"message": "please approve the order first "}

            if order.status == "In Transit":
                order.status = "completed"
                return {
                    "message":
                    "Your has been order completed awaiting delivery"
                }

        return {"message": "Order not found"}, 404


class MarkOrderInTransit(Resource):

    @jwt_required
    def put(self, id):
        '''mark order has started being transported'''
        order = Order().get_by_id(id)

        if order:
            if order.status == "completed" or order.status == "declined":
                return {"You already marked the order as {}".format(order.status)}, 200

            if order.status == "Pending":
                return {"message": "please approve the order first"}, 200

            if order.status == "approved":
                order.status = "In Transit"
                return {"message": "The order is now on the road!Rember to keep track of the order"}, 200

        return {"message": "The order could not be found!,check on the id please"}, 404


class DeclineOrder(Resource):

    @jwt_required
    def put(self, id):
        '''decline a specific order'''

        order = Order().get_by_id(id)

        if order:

            if order.status != "Pending":
                return {"message": "order already {}".format(order.status)}

            order.status = "declined"
            return {"message": "Order declined"}

        return {"message": "Order not found"}, 404
