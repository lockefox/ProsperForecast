"""tests for health reporters"""

import pytest
import forecast._version as _version
def test_version(client):
    """validate /version endpoint"""

    rep = client.get('/api/v1/version')
    assert rep.status_code == 200

    assert rep.get_json()['version'] == _version.__version__
