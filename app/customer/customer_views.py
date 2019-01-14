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
        weight = int(data['weight'])
        current_location = origin
        price = weight * 10
        sender = get_jwt_identity()

        validate = validators.Validators()

        if destination.isdigit():
            return {"message":"Counter check the destination name"},400

        if type(destination) == int:
            return {"message":"destination can't be an interger"},400

        if not validate.valid_destination_name(destination):
            return {'message': "kindly have a look on the destination name once more"}, 400
        
        if origin.isdigit():
            return {"message":"Counter check the origin name"},400

        if type(origin) == int:
            return {"message":"origin can't be an interger"},400

        if not validate.valid_origin_name(origin):
            return {'message': "kindly have a look on the origin name once more"}, 400

        if type(weight) != int:
            return {'message': "Invalid weight"}, 400

        order = Parcel(sender, origin, current_location, destination, price, weight)
        order.add()
        return {
            "message": "keep tight!Your parcel order has been placed!",
            "order":order.json_order()
        }, 201



class GetOrders(Resource):

    @jwt_required
    def get(self):
        orders = Parcel().get_all_orders()

        if orders:
            return {"orders": [order.serialize() for order in orders]}, 200
        return {"message":"no orders were found"},404


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
        if orders:
            return {"In Transitorder": [order.serialize() for order in orders]}, 200
        return {"message":"no intransit orders were found"},404


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

        validate = validators.Validators()

        if destination.isdigit():
            return {"message":"destination cannot be only numbers"},400
        if not validate.valid_destination_name(destination):
            return {"message":"destination name looks invalid,kindly check"},400

        parcel = Parcel().get_by_id(id)

        if parcel:
            if parcel.status == 'Pending':
                parcel.destination = destination
                return {
                    'message': 'destination updated successfully',
                    'parcel':parcel.serialize()
                }, 200
            return {'message': 'parcel already {}'.format(parcel.status)}, 400
        return {'message': 'parcel not found'}, 404
    
class UpdateParcelOrigin(Resource):

    @jwt_required
    def put(self, id):
        '''update parcel origin '''

        data = request.get_json()
        origin = data['origin']

        validate = validators.Validators()
        if origin.isdigit():
            return {"message":"origin cannot be only numbers"},400
        if not validate.valid_destination_name(origin):
            return {"message":"origin name looks invalid,kindly check"},400

        parcel = Parcel().get_by_id(id)

        if parcel:
            if parcel.status == 'Pending':
                parcel.origin = origin
            
                return {
                    'message': 'origin updated successfully',
                    'parcel':parcel.serialize()
                }, 200
            return {'message': 'parcel already {}'.format(parcel.status)}, 400
        return {'message': 'parcel not found'}, 404
    
class UpdateParcelWeight(Resource):

    @jwt_required
    def put(self, id):
        '''update parcel origin '''

        data = request.get_json()
        weight = int(data['weight'])
        price = weight * 10

        validate = validators.Validators()

        if type(weight) != int:
            return {"message":"weight can only be an interger"},400

        parcel = Parcel().get_by_id(id)

        if parcel:
            if parcel.status == 'Pending':
                parcel.weight = weight
                parcel.price = price
                return {
                    'message': 'weight and price updated successfully',
                    'parcel':parcel.serialize()
                }, 200
            return {'message': 'parcel already {}'.format(parcel.status)}, 400
        return {'message': 'parcel not found'}, 404
    
   
    

