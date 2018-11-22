from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import User, Parcel

class SpecificUserorders(Resource):
    
    @jwt_required
    def get(self, id):
       ''' get parcels for a specific user '''
       user = User().get_by_id(id)

       if user:
            orders = Parcel().orders_by_sender(user.username)
            if orders:
               all_orders = [order.serialize() for order in orders]
               return {'orders': all_orders}, 200
            return {'message':'{} has no orders for now'.format(user.username)}, 404
       return {'message':'user with id {} does not exist'.format(id)},404
