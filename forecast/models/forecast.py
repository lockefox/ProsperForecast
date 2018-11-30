"""sqlalchemy schemas for Forecast endpoints"""
from datetime import datetime
from forecast.extensions import db
from flask_jwt_extended import get_jwt_identity
class ForecastModel(db.Model):
    """request model"""
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False,
    )
    ticker = db.Column(
        db.String(16),
        nullable=False,
    )
    request_range = db.Column(
        db.Integer,
        nullable=False,
    )
    forecast_range = db.Column(
        db.Integer,
        nullable=False,
    )
    request_datetime = db.Column(
        db.DateTime,
        nullable=False,
    )
    status = db.Column(
        db.Text,
    )

    def __init__(
            self,
            ticker,
            request_range=600,
            forecast_range=60,
            **kwargs,
    ):
        """load that data"""
        self.user_id = get_jwt_identity()
        self.request_datetime = datetime.utcnow()
        self.ticker = ticker
        self.request_range = request_range
        self.forecast_range = forecast_range
        self.status = 'INIT'
