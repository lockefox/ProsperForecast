"""version/status/health endpoints for rest API"""

import flask_restful
import flask_jwt_extended

import forecast._version as _version

class VersionResource(flask_restful.Resource):
    """return the current deployed version"""
    #method_decorators = [flask_jwt_extended.jwt_required]

    def get(self):
        """HTTP GET: version info"""
        return dict(
            version=_version.__version__,
        )
