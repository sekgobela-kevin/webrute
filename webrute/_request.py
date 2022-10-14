import requests
import aiohttp

import numbers


class Request():
    """Fake request class for keeping request information"""
    _supported_attrs = (
        "method", "url", "params", "data", "headers", "cookies", 
        "files", "auth", "timeout","allow_redirects", "proxies",
        "hooks", "stream", "verify", "cert", "json",
    )

    def __init__(    
        self,    
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None):
        self.method = method
        self.url = url
        self.params = params
        self.data = data
        self.headers = headers
        self.cookies = cookies
        self.files = files
        self.auth= auth
        self.timeout = timeout
        self.allow_redirects = allow_redirects
        self.proxies = proxies
        self.hooks = hooks
        self.stream = stream
        self.verify= verify
        self.cert = cert
        self.json = json

    def to_dict(self):
        # Converts request attributes into dict compatible with 'requests'.
        # Only attributes that are not None get included.
        attrs_dict = {}
        for attr in self._supported_attrs:
            attr_val =  getattr(self, attr)
            if attr_val is not None:
                attrs_dict[attr] = attr_val
        return attrs_dict
    
    def to_adict(self):
        # Converts request attributes to dict compatible with 'aiohttp'.
        attrs_dict = self.to_dict().copy()
        if "proxies" in attrs_dict:
            attrs_dict["proxy"] = list(self.proxies.items())[0]
            del attrs_dict["proxies"]
        if "files" in attrs_dict:
            attrs_dict["file"] = list(self.files.items())[-1]
            attrs_dict["data"] = attrs_dict.get("data", {})
            attrs_dict["data"].update(self.files)
            del attrs_dict["files"]
        if "timeout" in attrs_dict:
            timeout = attrs_dict["timeout"]
            if isinstance(timeout, numbers.Number):
                attrs_dict["timeout"] = aiohttp.ClientTimeout(timeout)
            else:
                conn_timeout = timeout[0]
                read_timeout = timeout[1]
                attrs_dict["timeout"] = aiohttp.ClientTimeout(
                    connect=conn_timeout,
                    sock_read=read_timeout
                )

        # Changes 'veryfy' to 'verify_ssl' and 'cert' to 'ssl'.
        if "verify" in attrs_dict:
            attrs_dict["verify_ssl"] = attrs_dict["verify"]
            del attrs_dict["verify"]
        if "cert" in attrs_dict:
            attrs_dict["ssl"] = attrs_dict["cert"]
            del attrs_dict["cert"]
        return attrs_dict

    @classmethod
    def is_supported(cls, attribute):
        return attribute in cls._supported_attrs

    def get_value(self, attr):
        if self.is_supported(attr):
            return getattr(self, attr)

    def get_key(self, attr_value):
        attrs_dict = self.to_dict()
        attr_values = list(attrs_dict.values())
        try:
            # Tries to get index of attribute value
            index = attr_values.index(attr_value)
        except IndexError:
            pass
        else:
            # Uses the index to get corresponding attribute(key)
            return list(attrs_dict.keys())[index]

    def copy(self):
        return self.__class__(**self.to_dict())

        
class RequestPost(Request):
    def __init__(self, url, **kwargs) -> None:
        super().__init__("POST", url, **kwargs)

class RequestGet(Request):
    def __init__(self, url, **kwargs) -> None:
        super().__init__("GET", url, **kwargs)

class RequestDelete(Request):
    def __init__(self, url, **kwargs) -> None:
        super().__init__("DELETE", url, **kwargs)

class RequestPut(Request):
    def __init__(self, url, **kwargs) -> None:
        super().__init__("PUT", url, **kwargs)
    

    


