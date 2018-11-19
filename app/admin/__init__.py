from flask import Blueprint
from .admin_views import *

admin_blueprint=Blueprint("admin", __name__)