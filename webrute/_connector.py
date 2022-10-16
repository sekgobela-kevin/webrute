from webrute import _session
from webrute import _response
from webrute import _request

import broote


class Connector():
    def __init__(self, custom_request, session=None):
        self._custom_request = custom_request
        self._session = session
        if session is None:
            self._session = self._create_session()
            self._session_created = True
        else:
            self._session_created = False

    def _create_session(self):
        return _session.create_session()

    def get_session(self):
        return self._session

    def connect(self):
        return self._session.request(self._custom_request)

    def close(self):
        if self._session_created:
            self._session.close()


class AsyncConnector(Connector):
    def __init__(self, custom_request, session=None):
        super().__init__(custom_request, session)

    def _create_session(self):
        return _session.create_asession()

    async def connect(self):
        return await self._session.request(self._custom_request)

    async def close(self):
        if self._session_created:
            await self._session.close()

def to_custom_request(request_info):
    if isinstance(request_info, dict):
        return _request.Request(**request_info)
    return request_info

def setup_connector(request_info, connector_type, session=None):
    custom_request = to_custom_request(request_info)
    return connector_type(custom_request, session)


if __name__ == "__main__":
    custom_request = _request.RequestGet("http://example.org/ws")
    connector = Connector(custom_request)
    print(connector.connect().get_text())