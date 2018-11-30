"""custom exceptions and warnings for project"""

class ForecastHTTPException(Exception):
    """class for containing `expected` exceptions

    Args:
        message (str): exception message
        http_code (int): HTTP status code

    """
    def __init__(self, message, http_code):
        self.message = message
        self.http_code = http_code

        Exception.__init__(self)

class ForecastWarning(UserWarning):
    """base warning for Forecast API"""

class SecretMissing(ForecastWarning):
    """expected a secret, none provided"""
