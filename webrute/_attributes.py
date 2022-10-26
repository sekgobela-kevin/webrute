from webrute import exceptions
from webrute import _util

import httpx


class Attributes():
    _unsupported_attrs = set()
    _supported_attrs = None
    _validate_attrs = True

    _default_attr = object()

    def __init__(self, **kwargs) -> None:
        if self._validate_attrs:
            self.raise_for_unsupported(kwargs)
        self._attrs_dict = kwargs

    def get_attr(self, attr, default=None):
        try:
            return self._attrs_dict[attr]
        except KeyError:
            return default
            # erro_msg = "Attribute '{}' does not exists"
            # raise exceptions.AttributeNotFound(erro_msg.format(attr))

    def get_attrs(self):
        return self._attrs_dict

    def get_attrs_keys(self):
        return tuple(self._attrs_dict.key())

    def get_attrs_values(self):
        return tuple(self._attrs_dict.values())

    def attr_exists(self, attr):
        return attr in self._attrs_dict

    @classmethod
    def attr_supported(cls, attr):
        if attr in cls._unsupported_attrs:
            return False
        elif cls._supported_attrs is None:
            return True
        return attr in cls._supported_attrs

    @classmethod
    def attrs_supported(cls, attrs, min_ratio=None):
        if min_ratio is not None:
            return all(map(cls.attr_supported, attrs))
        else:
            filtered_attrs = list(filter(cls.attr_supported, attrs))
            return min_ratio <= len(filtered_attrs)/len(attrs)

    @classmethod
    def get_supported_attrs(cls, attr):
        if cls._supported_attrs is None:
            return set()
        return cls._supported_attrs

    @classmethod
    def get_unsupported_attrs(cls, attr):
        return cls._unsupported_attrs

    @classmethod
    def raise_for_unsupported(cls, attrs):
        for attr in attrs:
            if not cls.attr_supported(attr):
                err_msg = "Attribute '{}' is not supported by '{}'"
                err_msg = err_msg.format(attr, cls.__name__)
                raise exceptions.UnsupportedAttribute(err_msg)

    def to_dict(self):
        return self._attrs_dict

    @classmethod
    def to_instance(cls, object_):
        # Creates instance of this type from provided object.
        if isinstance(object_, cls):
            return object_
        elif isinstance(object_, Attributes):
            return cls(**object_.get_attrs())
        elif isinstance(object_, dict):
            return cls(**object_)
        else:
            return cls(**dict(object_))
        

    def __add__(self, other):
        return type(self)({**self._attrs_dict, **other.get_attrs()})

    def copy(self):
        return type(self)(**self._attrs_dict)


class SessionAttrs(Attributes):
    _supported_attrs = set(_util.extract_arguments(httpx.Client, True))

class RequestAttrs(Attributes):
    # All arguments of httpx.request() are supported.
    _supported_attrs = set(_util.extract_arguments(httpx.request, True))

class RequestBodyAttrs(RequestAttrs):
    pass

class RequestNoBodyAttrs(RequestAttrs):
    # All arguments of httpx.get() or similar methods are supported.
    _supported_attrs = _util.extract_arguments(httpx.get, True)

    # All arguments of not supported by httpx.get() or similar methods.
    # {'data', 'json', 'content', 'files', 'method'}
    _unsupported_attrs = set(_util.extract_arguments(httpx.request, True))\
        .difference(_util.extract_arguments(httpx.get, True))


class RequestPostAttrs(RequestBodyAttrs):
    def __init__(self, **kwargs) -> None:
        kwargs["method"] = "POST"
        super().__init__(**kwargs)

class RequestPutAttrs(RequestBodyAttrs):
    def __init__(self, **kwargs) -> None:
        kwargs["method"] = "PUT"
        super().__init__(**kwargs)

class RequestGetAttrs(RequestNoBodyAttrs):
    def __init__(self, **kwargs) -> None:
        kwargs["method"] = "GET"
        super().__init__(**kwargs)


class RequestOptionAttrs(RequestNoBodyAttrs):
    def __init__(self, **kwargs) -> None:
        kwargs["method"] = "OPTION"
        super().__init__(**kwargs)

class RequestDeleteAttrs(RequestNoBodyAttrs):
    def __init__(self, **kwargs) -> None:
        kwargs["method"] = "DELETE"
        super().__init__(**kwargs)



if __name__ == "__main__":
    attrs_obj = SessionAttrs(headers="header")
    print(attrs_obj.get_attrs())
    print(attrs_obj.get_attr("hesaders", object))
