from flask import Blueprint
from flask_restful import Api

from forecast.api.resources import *

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(VersionResource, '/version')
api.add_resource(StockForecast, '/stock')
