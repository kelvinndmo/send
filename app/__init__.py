from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS,cross_origin
from config import app_config
from flask_jwt_extended import JWTManager
from .customer.customer_views import PostParcel, UpdateParcelDestination, CancelOrder,UpdateParcelWeight, GetOrders, SpecificOrder,UpdateParcelOrigin, InTransitOrders, GetAcceptedOrders, DeclinedOrders, CompletedOrders
from .admin.admin_views import CompleteOrder, AcceptStatus, MarkOrderInTransit, DeclineOrder, UpdateLocation
from app.auth.auth_views import Login, Signup
from .userorders.user_order import SpecificUserorders


jwt = JWTManager()


def create_app(config_stage):
    '''creates the app'''

    app = Flask(__name__)
    app.config.from_object(app_config[config_stage])
    
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    

    jwt.init_app(app)
    

    from .admin import admin_blueprint
    admin = Api(admin_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix="/api/v2/parcels")

    from .auth import auth_blueprint
    auth = Api(auth_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix="/api/v2/auth")

    from .customer import customer_blueprint
    customer = Api(customer_blueprint)
    app.register_blueprint(customer_blueprint, url_prefix="/api/v2/parcels")

    from .userorders import userorders_blueprint
    userorders = Api(userorders_blueprint)
    app.register_blueprint(userorders_blueprint, url_prefix="/api/v2/users")

    auth.add_resource(Signup, '/signup')
    auth.add_resource(Login, '/login')
    customer.add_resource(SpecificOrder, '/<int:id>')
    customer.add_resource(UpdateParcelDestination, '/<int:id>/destination')
    customer.add_resource(UpdateParcelWeight, '/<int:id>/weight')
    customer.add_resource(UpdateParcelOrigin, '/<int:id>/origin')
    customer.add_resource(PostParcel, '')
    customer.add_resource(GetOrders, '')
    customer.add_resource(GetAcceptedOrders, '/acceptedorders')
    admin.add_resource(CompleteOrder, '/<int:id>/completed')
    admin.add_resource(UpdateLocation, '/<int:id>/presentlocation')
    customer.add_resource(CompletedOrders, '/completedorders')
    customer.add_resource(DeclinedOrders, '/declined')
    userorders.add_resource(SpecificUserorders, '/<int:id>/parcels')
    admin.add_resource(AcceptStatus, '/<int:id>/approved')
    admin.add_resource(MarkOrderInTransit, '/<int:id>/intransit')
    customer.add_resource(InTransitOrders, '/intransit')
    customer.add_resource(CancelOrder, '/<int:id>/cancel')
    admin.add_resource(DeclineOrder, '/<int:id>/declined')

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify(
            {
                "message":"Kindly please check the URL,its incorrect"
            }
        ), 404

    return app
