from flask import Flask, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import User, Parcel
from utils import validators
import datetime


class PostParcel(Resource):
    '''place parcel order.'''

    @jwt_required
    def post(self):
        '''place a new parcel'''

        data = request.get_json()
        origin = data['origin']
        destination = data['destination']
        weight = data['weight']
        current_location = origin
        price = weight * 10
        sender = get_jwt_identity()

        validate = validators.Validators()

        if not validate.valid_destination_name(destination):
            return {'message': "destination is invalid"}, 400

        if not validate.valid_origin_name(origin):
            return {'message': "invalid origin name"}, 400

        if type(price) != int:
            return {'message': "Invalid price"}, 400

        if type(weight) != int:
            return {'message': "Invalid weight"}, 400

        order = Parcel(sender, origin, current_location, destination, price, weight)
        order.add()
        return {
            "message": "keep tight!Your parcel order has been placed!",
            "parcel":order.serialize()
        }, 201


class GetOrders(Resource):

    @jwt_required
    def get(self):
        orders = Parcel().get_all_orders()
        return {"orders": [order.serialize() for order in orders]}


class SpecificOrder(Resource):
    '''fetch a specific parcel order by id'''

    @jwt_required
    def get(self, id):
        '''get a specific order by id'''

        order = Parcel().get_by_id(id)

        if order:
            return {"order": order.serialize()}, 200

        return {"message": "order of id {} not found".format(id)}, 404


class InTransitOrders(Resource):

    @jwt_required
    def get(self):

        orders = Parcel().intransit_orders()
        return {"In Transitorder": [order.serialize() for order in orders]}


class DeclinedOrders(Resource):

    @jwt_required
    def get(self):
        ''''return a list of decloned orders'''

        orders = Parcel().declined_orders()
        if orders:
            return {
                "declined orders": [order.serialize() for order in orders]
            }
        return {"message": "no declined orders were found"}, 404


class CompletedOrders(Resource):

    @jwt_required
    def get(self):
        '''return a list of parcel orders completed by admin'''

        orders = Parcel().completed_orders()

        if orders:
            return {"completed orders": [
                order.serialize() for order in orders
            ]
            }, 200
        return {"message": "no completed orders were found"}, 404


class CancelOrder(Resource):

    @jwt_required
    def put(self, id):
        '''cancel a specific order by id'''

        order = Parcel().get_by_id(id)
        if order:
            if order.status == "canceled":
                return {"message": "order already cancelled"}, 400
            if order.status != "cancelled" and order.status != "Pending":
                return {"message": "order already {}".format(order.status)}, 400
            order.cancel_order(id)
            return {"messsage": "order successfully cancelled"}, 200

        return {"message": "order of id {} not found".format(id)}, 404


class GetAcceptedOrders(Resource):

    @jwt_required
    
    def get(self):
        '''return list of approved orders'''

        orders = Parcel().accepted_orders()

        return {
            "approved_orders": [
                order.serialize() for order in orders
                if order.status == "accepted"
            ]
        }, 200


class UpdateParcelDestination(Resource):

    @jwt_required
    def put(self, id):
        '''update parcel destination '''

        data = request.get_json()
        destination = data['destination']

        parcel = Parcel().get_by_id(id)

        if parcel:
            if parcel.status != 'pending':
                parcel.destination = destination
                return {
                    'message': 'destination updated successfully',
                    'parcel':parcel.serialize()
                }, 200
            return {'message': 'parcel already {}'.format(parcel.status)}, 400
        return {'message': 'parcel not found'}, 404