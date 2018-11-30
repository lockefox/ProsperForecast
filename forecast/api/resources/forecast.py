"""generate forecasts for given tickers"""
import logging

import flask_restful
import marshmallow
import pandas
import requests

from flask import current_app as app  # https://stackoverflow.com/a/52678595
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from forecast.extensions import ma, db
from forecast.models.forecast import ForecastModel
import forecast.exceptions as exceptions
import forecast._version as _version


def get_history_from_robinhood(
        ticker,
        request_range=600,
        bounds='regular',
        resource_uri='https://api.robinhood.com/quotes/historicals/',
        **kwargs
):
    """generate stock history from robinhood

    Args:
        ticker (str): stock ticker to request from Robinhood
        request_range (int): days of data to return (300 trading days/yr)
        bounds (str): what daily bounds to use (https://bit.ly/2DVbdxD)
        resource_uri (str): endpoint to request data from
        **kwargs: used as buffer for Marshmallow schema.data

    Returns:
        pandas.DataFrame: trimmed data from endpoint
            [begins_at, open_price, close_price, high_price, low_price,
            volume, session, interpolated]

    Raises:
        requests.RequestsException: unable to generate historical data

    """
    params = dict(
        symbols=ticker,
        interval='day',
        bounds=bounds,
    )
    req = requests.get(
        resource_uri,
        params=params,
    )
    req.raise_for_status()
    return pandas.DataFrame(req.json()['results'][0]['historicals'])\
        .head(request_range)

def generate_error(
        message,
        http_code,
        metadata=None,
        logger=logging.getLogger(_version.__library_name__),
):
    """generate an error report

    Args:
        message (str): information about crash
        http_code (int): what HTTP code to return to user
        metadata (:obj:`flask_marshmallow.Schema`): current request data
        logger (:obj:`logging.logger`): logging handle for error alerting

    Returns:
        dict, int: a JSON/http-code pair for Flask-Restful

    """
    if metadata:
        logger.error(message, exc_info=True)
        metadata.status = f'ERROR - {message}'
        db.session.add(metadata)
        db.session.commit()

    return {'ERROR': message}, http_code

class ForecastSchema(ma.Schema):

    ticker = ma.String(required=True)
    request_range = ma.Integer(default=600)
    forecast_range = ma.Integer(default=60)
    bounds = ma.String(
        default='regular',
        validate=marshmallow.validate.OneOf(['extended', 'regular', 'trading']),
    )


    class Meta:
        model = ForecastModel
        sqla_session = db.session


class StockForecast(flask_restful.Resource):
    method_decorators = [jwt_required]
    schema = ForecastSchema()
    model = ForecastModel

    def __init__(self):
        self.data = self.schema.load(request.args.to_dict())


    def get(self):
        if self.data.errors:
            return generate_error(f'Invalid args - {self.data.errors}', 400,)
        metadata = self.model(**self.data.data)
        app.logger.info(self.data)

        ## Generate Historical data ##
        try:
            history = get_history_from_robinhood(**self.data.data)
        except Exception as err:
            return generate_error(
                f'Unable to generate historical data from RH {err!r}', 500, metadata=metadata)


        ## Happy path finished ##
        metadata.status = 'SUCCESS'
        db.session.add(metadata)
        db.session.commit()
        return history.to_dict(orient='records')
