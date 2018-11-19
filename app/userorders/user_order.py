from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


class SpecificUserorders(Resource):
    
    @jwt_required
    def get(self, id):
       return {"orders":[order.serialize() for order in orders if get_jwt_identity() == id]}
