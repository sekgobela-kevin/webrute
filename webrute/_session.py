from webrute import _response
from webrute import _request
import requests
import aiohttp
import requests_html

import asyncio


class Session():
    '''Composites session object of libraries for performing request'''
    def __init__(self, request_session):
        self._request_session = request_session
        self._request_session: requests.Session()

    def get_session(self):
        return self._request_session

    def set_verify(self, verify):
        raise NotImplementedError

    def set_auth(self, auth):
        raise NotImplementedError

    def set_headers(self, headers):
        raise NotImplementedError

    def set_proxies(self, proxies):
        raise NotImplementedError

    def set_cookies(self, cookies):
        raise NotImplementedError


    def get_verify(self):
        raise NotImplementedError

    def get_auth(self):
        raise NotImplementedError

    def get_headers(self):
        raise NotImplementedError

    def get_proxies(self):
        raise NotImplementedError

    def get_cookies(self):
        raise NotImplementedError

    def get_cookies(self):
        raise NotImplementedError


    def clear_cookies(self):
        self.get_cookies().clear()

    def close(self):
        self._request_session.close()

    def request(self, custom_request, method=None):
        raise NotImplementedError

    def post(self, custom_request):
        return self.request(custom_request)

    def get(self, custom_request):
        return self.request(custom_request)

    def put(self, custom_request):
        return self.request(custom_request)

    def delete(self, custom_request):
        return self.request(custom_request)


class AsyncSession(Session):
    '''Composites session object of async request libraries'''
    async def request(self, custom_request, method=None):
        raise NotImplementedError

    async def post(self, custom_request):
        return await self.request(custom_request, "POST")

    async def get(self, custom_request):
        return await self.request(custom_request, "GET")

    async def put(self, custom_request):
        return await self.request(custom_request, "PUT")

    async def delete(self, custom_request):
        return await self.request(custom_request, "DELETE")

    async def close(self):
        await self._request_session.close()


class RequestsLikeSession(Session):
    '''Composites session object of requests related libs(e.g requests)'''
    def __init__(self, request_session):
        super().__init__(request_session)
        self._request_session: requests.Session

    def set_verify(self, verify):
        self._request_session.verify  = verify

    def set_auth(self, auth):
        self._request_session.auth  = auth

    def set_headers(self, headers):
        self._request_session.headers  = headers

    def set_proxies(self, proxies):
        self._request_session.proxies  = proxies

    def set_cookies(self, cookies):
        self._request_session.cookies  = cookies


    def get_verify(self):
        return self._request_session.verify

    def get_auth(self):
        return self._request_session.auth

    def get_headers(self):
        return self._request_session.headers

    def get_proxies(self):
        return self._request_session.proxies

    def get_cookies(self):
        return self._request_session.cookies

    def clear_cookies(self):
        self.get_cookies().clear()

    def request(self, custom_request, method=None):
        kwargs = custom_request.to_dict()
        if method is not None:
            kwargs["method"] = method
        response = self._request_session.request(**kwargs)
        return _response.requests_libraries_response(response, self)

    def close(self):
        self._request_session.close()


class RequestsSession(RequestsLikeSession):
    '''Composites session object for well known requests library'''
    def __init__(self, request_session):
        super().__init__(request_session)

    def request(self, custom_request, method=None):
        kwargs = custom_request.to_dict()
        if method is not None:
            kwargs["method"] = method
        response = self._request_session.request(**kwargs)
        return _response.requests_response(response, self)


class RequestsHTMLSession(RequestsSession):
    '''Composites session object for requests_html library(non async)'''
    def __init__(self, request_session):
        super().__init__(request_session)
        self._request_session: requests_html.HTMLSession


class AsyncRequestsHTMLSession(RequestsHTMLSession):
    '''Composites async session object for requests_html library'''
    def __init__(self, request_session):
        super().__init__(request_session)
        self._request_session: requests_html.AsyncHTMLSession

    async def request(self, custom_request, method=None):
        kwargs = custom_request.to_dict()
        if method is not None:
            kwargs["method"] = method
        future = self._request_session.request(**kwargs)
        await asyncio.wait(future)
        response = future.result()
        return _response.requests_html_response(response, self)

    async def post(self, custom_request):
        return await self.request(custom_request, "POST")

    async def get(self, custom_request):
        return await self.request(custom_request, "GET")

    async def put(self, custom_request):
        return await self.request(custom_request, "PUT")

    async def delete(self, custom_request):
        return await self.request(custom_request, "DELETE")

    def run(self, *coros):
        return self._request_session.run(*coros)

    async def close(self):
        self._request_session.close()


class AiohttpSession(AsyncSession):
    '''Composites session object for aiohttp library'''
    def __init__(self, request_session):
        super().__init__(request_session)
        self._request_session: aiohttp.ClientSession


    async def request(self, custom_request, method=None):
        kwargs = custom_request.to_adict()
        if method is not None:
            kwargs["method"] = method
        response = await self._request_session.request(**kwargs)
        return _response.aiohtml_response(response, self)


class RequestSession(RequestsSession):
    """Session based on 'requests' library"""
    pass

class AsyncRequestSession(AiohttpSession):
    """Session based on 'aiohttp' library"""
    pass

def create_session():
    """Creates session for requests library"""
    session_ = requests.Session()
    return RequestSession(session_)

def create_asession(*args, **kwargs):
    """Creates session for aiohttp library"""
    session_ = aiohttp.ClientSession(*args, **kwargs)
    return AsyncRequestSession(session_)

def create_render_session(*args, **kwargs):
    """Creates session for requests_html session(non asyncio)"""
    session_ = requests_html.HTMLSession(*args, **kwargs)
    return RequestsHTMLSession(session_)

def create_render_asession(*args, **kwargs):
    """Creates session for requests_html session(asyncio)"""
    session_ = requests_html.AsyncHTMLSession(*args, **kwargs)
    return AsyncRequestsHTMLSession(session_)




if __name__ == "__main__":

    async def main():
        session = create_asession()
        custom_request = _request.RequestGet("https://www.example.com/")
        response = await session.request(custom_request)
        print(await response.get_bytes())
        await session.close()
        

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())