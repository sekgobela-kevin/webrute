import requests
import aiohttp
import requests_html


class response():
    """Composites response object of request library"""
    def __init__(self, request_response, session=None):
        self._request_response = request_response
        self._session = session

    def get_session(self):
        return self._request_response

    def get_session(self):
        return self._session

    def get_json(self):
        raise NotImplementedError

    def get_cookies(self):
        raise NotImplementedError

    def get_url(self):
        raise NotImplementedError

    def get_headers(self):
        raise NotImplementedError

    def get_elapsed_time(self):
        raise NotImplementedError

    def get_status_code(self):
        raise NotImplementedError

    def get_length(self):
        raise self.get_headers().get("Content-Length", None)

    def get_encoding(self):
        raise NotImplementedError

    def get_stream(self):
        raise NotImplementedError

    def read(self, size=None):
        stream = self.get_stream()
        if hasattr(stream, "seek"):
            stream.seek(0)
        if size != None:
            return stream.read(size)
        return stream.read()

    def get_bytes(self):
        return self.read()

    def get_text(self):
        raise NotImplementedError

    def has_errors(self):
        return self.get_status_code() > 400

    def is_success(self):
        return self.get_status_code() == 200

    def is_redirect(self):
        status = self.get_status_code()
        raise status <= 300 or status <= 399

    def close(self):
        self._request_response.close()


class async_responce(response):
    """Composites response object of async request library"""
    def __init__(self, request_response, session=None):
        super().__init__(request_response, session)

    async def get_stream(self):
        raise NotImplementedError

    async def read(self, size=None):
        stream = await self.get_stream()
        if hasattr(stream, "seek"):
            stream.seek(0)
        if size != None:
            return await stream.read(size)
        return await stream.read()

    async def get_bytes(self):
        raise NotImplementedError

    async def get_text(self):
        raise NotImplementedError


class requests_libraries_response(response):
    """Composites response object of 'requests' like library"""
    def __init__(self, request_response, session=None):
        super().__init__(request_response, session)
        self._request_response: requests.Response

    def get_url(self):
        return self._request_response.url

    def get_cookies(self):
        return self._request_response.cookies

    def get_json(self):
        return self._request_response.json()

    def get_headers(self):
        return self._request_response.headers

    def get_elapsed_time(self):
        return self._request_response.elapsed.total_seconds

    def get_status_code(self):
        return self._request_response.status_code

    def get_encoding(self):
        return self._request_response.encoding

    def get_stream(self):
        return self._request_response.raw

    def get_bytes(self):
        return self._request_response.content

    def get_text(self):
        return self._request_response.text

    def is_redirect(self):
        return self._request_response.is_redirect


class requests_response(requests_libraries_response):
    """Composites response object of well known requests library"""
    def __init__(self, request_response, session=None):
        super().__init__(request_response, session)



class requests_html_response(requests_libraries_response):
    """Composites response object of requests_html library"""
    def __init__(self, request_response, session=None, render=False):
        super().__init__(request_response, session)
        self._request_response: requests_html.HTMLResponse



class aiohtml_response(async_responce):
    """Composites response object of aiohtml library"""
    def __init__(self, request_response, session=None):
        super().__init__(request_response, session)
        self._request_response: aiohttp.ClientResponse

    def get_url(self):
        return self._request_response.url

    def get_cookies(self):
        return self._request_response.cookies

    def get_json(self):
        return self._request_response.json

    def get_headers(self):
        return self._request_response.headers

    def get_status_code(self):
        return self._request_response.status

    def get_encoding(self):
        return self._request_response.get_encoding()

    def get_content_length(self):
        return self._request_response.content_length

    async def get_bytes(self):
        return await self.read()

    async def get_text(self):
        return await self._request_response.text()

    async def get_stream(self):
        return self._request_response.content


