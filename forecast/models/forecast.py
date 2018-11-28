from forecast.extensions import db

class ForecastModel(db.Model):
    """request model"""
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        unique=True,
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
    outcome = db.Column(
        db.Text,
    )
