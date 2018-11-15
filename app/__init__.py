from flask import Flask
from flask_restful import Api
from config import app_config
from flask_jwt_extended import JWTManager
from .customer.customer_views import PostParcel,CancelOrder, SpecificUserorders, GetOrders, SpecificOrder, InTransitOrders, GetAcceptedOrders, DeclinedOrders, CompletedOrders
from .admin.admin_views import CompleteOrder, AcceptStatus, MarkOrderInTransit, DeclineOrder
from app.auth.auth_views import Login, SignUp


jwt = JWTManager()


def create_app(config_stage):
    '''creates the app'''

    app = Flask(__name__)
    app.config.from_object(app_config[config_stage])

    jwt.init_app(app)


    api = Api(app)

    api.add_resource(SignUp, '/api/v1/auth/signup')
    api.add_resource(Login, '/api/v1/auth/login')
    api.add_resource(SpecificOrder, '/api/v1/parcels/<int:id>')
    api.add_resource(PostParcel, '/api/v1/parcels')
    api.add_resource(GetOrders, '/api/v1/parcels')
    api.add_resource(GetAcceptedOrders, '/api/v1/acceptedorders')
    api.add_resource(CompleteOrder, '/api/v1/parcels/<int:id>/completed')
    api.add_resource(CompletedOrders, '/api/v1/parcels/completedorders')
    api.add_resource(DeclinedOrders, '/api/v1/parcels/declined')
    api.add_resource(SpecificUserorders, '/users/<int:id>/parcels')
    api.add_resource(AcceptStatus, '/api/v1/parcels/<int:id>/approved')
    api.add_resource(MarkOrderInTransit, '/api/v1/parcels/<int:id>/intransit')
    api.add_resource(InTransitOrders, '/api/v1/parcels/intransit')
    api.add_resource(CancelOrder, '/parcels/<int:id>/cancel')
    api.add_resource(DeclineOrder, '/api/v1/parcels/<int:id>/declined')

    return app
