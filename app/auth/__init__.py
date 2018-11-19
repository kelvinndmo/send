from flask import Blueprint
from .auth_views import *

auth_blueprint=Blueprint("auth", __name__)