from flask import Blueprint
from .customer_views import *

customer_blueprint=Blueprint("customer", __name__)