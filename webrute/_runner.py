from webrute import _request
from webrute import _connect

import broote


def setup_connector(request_info, connector_type, session=None):
    if isinstance(request_info, dict):
        custom_request = _request.Request(**request_info)
    else:
        custom_request = request_info
    return _connect.Connector(custom_request, session)


class web_basic_runner(broote.basic_runner):
    def __init__(self, request_info, table, **kwargs):
        connector = setup_connector(request_info, _connect.Connector)