"""generate forecasts for given tickers"""
from datetime import datetime as dt
import flask_restful
import marshmallow
from flask import current_app as app  # https://stackoverflow.com/a/52678595
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from forecast.extensions import ma, db
from forecast.models.forecast import ForecastModel
import forecast.exceptions as exceptions



class ForecastSchema(ma.Schema):

    ticker = ma.String(required=True)
    request_range = ma.Integer(default=600)
    forecast_range = ma.Integer(default=60)
    user_id = ma.Integer()
    request_datetime = ma.DateTime()

    class Meta:
        model = ForecastModel
        sqla_session = db.session

    @marshmallow.pre_load
    def get_metadata(self, data):
        data['user_id'] = get_jwt_identity()
        data['request_datetime'] = dt.utcnow().isoformat()
        return data


class StockForecast(flask_restful.Resource):
    method_decorators = [jwt_required]

    def __init__(self):
        self.schema = ForecastSchema()

    def get(self):
        data = self.schema.load(request.args.to_dict())
        marshmallow.pprint(data)
        app.logger.info(data.data)
