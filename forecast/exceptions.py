"""custom exceptions and warnings for project"""


class ForecastWarning(UserWarning):
    """base warning for Forecast API"""

class SecretMissing(ForecastWarning):
    """expected a secret, none provided"""
