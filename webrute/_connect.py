from webrute import _session
from webrute import _response
from webrute import _request

import broote


class Connector():
    def __init__(self, custom_response, session=None):
        self._custom_response = custom_response
        self._session = session
        if session is None:
            self._session = self._create_session()
            self._session_created = True
        else:
            self._session_created = False

    def _create_session(self):
        return _session.create_session()

    def connect(self):
        return self._session.request(self._custom_response)

    def close(self):
        if self._session_created:
            self._session.close()


class AsyncConnector(Connector):
    def __init__(self, custom_response, session=None):
        super().__init__(custom_response, session)

    def _create_session(self):
        return _session.create_asession()

    async def connect(self):
        return await self._session.request(self._custom_response)

    async def close(self):
        if self._session_created:
            await self._session.close()


if __name__ == "__main__":
    custom_request = _request.RequestGet("http://example.org/ws")
    connector = Connector(custom_request)
    print(connector.connect().get_text())