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

        order = Parcel(sender, origin, destination, price, weight)
        order.add()
        return {
            "message": "keep tight!Your parcel order has been placed!"
        }, 201

class GetOrders(Resource):
    
    @jwt_required
    def get(self):
        orders = Parcel().get_all_orders()
        return {"orders": [order.serialize() for order in orders]}

