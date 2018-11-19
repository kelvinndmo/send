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
        if not user.is_admin:
            return {'message': 'Your cannot access this level'}, 401
        return f(*args, **kwargs)

    return wrapper_function


class AcceptStatus(Resource):

    @jwt_required
    def put(self, id):
        '''mark an order as approved by admin'''

        order = Parcel().get_by_id(id)

        if order:
            if order.status != "Pending":
                return {"message": "order already {}".format(order.status)}, 200
            order.accept_status(id)
            return {"message": "your order has been approved"}, 200
        return {"message": "order not found"}, 404
        


