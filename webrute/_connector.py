from webrute import _attributes

import webrute
import httpx


class Connector():
    _session_type = httpx.Client

    def __init__(self, target, session=None) -> None:
        # Store target and session before being overiden
        self._original_target = target
        self._original_session = session

        # Setup target and session by overiding.
        self._target = self._setup_target(target)
        self._session = self._setup_session(session)
        self._callable_session = self._setup_callable_session(session)

    @classmethod
    def _setup_target(cls, target):
        # Setupstarget to ensure its in right format and type.
        # Avoid using 'self' here as method is called by initializer.
        return cls.create_target(target)

    @classmethod
    def _setup_session(cls, session):
        # Setups httpx client session(real session not callable)
        return cls._setup_callable_session(session)()

    @classmethod
    def _setup_callable_session(cls, session):
        # Setups httpx client session wrapped within function.
        # Function is better a it lets 'broote' creates session itself.
        if session is None:
            # Better create session other than leaving it None.
            return lambda: cls._session_type()
        else:
            # Session is set to function
            return cls.create_callable_session(session) 


    @classmethod
    def create_callable_session(cls, session):
        # Creates session wrapped withon callable object(function)
        return lambda: cls.create_session(session) 
    
    @classmethod
    def create_session(cls, session):
        # Creates session from object that was passed as session.
        # session is whatever object that was passed as session.
        # It could be httpx.Client, dict, callable, etc.
        if isinstance(session, cls._session_type):
            return session
        elif isinstance(session, dict):
            return cls._session_type(**session)
        elif callable(session):
            return session()
        else:
            err_msg = "Session should be of type 'dict' or '{}' not '{}'"
            err_msg = err_msg.format(
                cls._session_type.__name__,
                type(session).__name__
            )
            raise TypeError(err_msg)

    @classmethod
    def create_target(cls, target):
        # Creates target from object that was passed as target.
        # Target can be str, bytes or dict.
        if isinstance(target, (str, bytes)):
            # String or bytes target will be taken as GET request.
            return {"url": target, "method": "GET"}
        elif isinstance(target, dict):
            return target
        else:
            err_msg = "Target should be any of types ('str, 'bytes', " +\
                "'dict' not {}"
            err_msg = err_msg.format(type(target).__name__)
            raise TypeError(err_msg)

    @classmethod
    def guess_connector_method(cls, connector_args, methods=("GET","POST")):
        # Guesses connector/request method from connector arguments
        if "method" in connector_args:
            # No need to guess when method already exists.
            return connector_args["method"]
        
        # Ensures that connector arguments are set(mosly will be dict)
        connector_args = set(connector_args)

        # Checks if connector arguments are GET request like.
        # This done by checking if POST like specific argument exist.
        unsupported = _attributes.RequestNoBodyAttrs.get_unsupported_attrs()
        if connector_args.intersection(unsupported):
            return methods[0]

        # Its likely POST request like method but cant be sure.
        # First check if atleast 50% of arguments are supported.
        elif _attributes.RequestAttrs._supported_attrs(connector_args, 0.5):
            return methods[1]


    @classmethod
    def transform_record(cls, record, method):
        # Transforms record into one supported by connector.
        # 'broote' now support record transformer.
        # Its only developer who knows how to transform record.
        method = method.lower()
        if method in  {"POST", "PUT"}:
            return webrute.record({"data": record})
        elif method in {"GET", "OPTION", "DELETE"}:
            return webrute.record({"params": record})
        else:
            return record

    def transform_connector_arguments(cls, connector_args):
        # Transforms connector arguments to be compatible with connector.
        method = cls.guess_connector_method(connector_args)
        if method: 
            connector_args = connector_args.copy()
            connector_args["method"] = method
        return connector_args

    @classmethod
    def create_connector_arguments(cls, target, record):
        # Creates arguments to be used when perfoming making request.
        # Target needs to be transformed to make it compatible with request.
        target_dict = cls.create_target(target)
        # Tries to get method from target if exists.
        #target_method = target_dict.get("method", None)
        # Transforms record to be compatible with request methods.
        # Not guaranteed to be compatible(just take it as compatible)
        #record_dict = cls.transform_record(record, target_method)
        record_dict = record

        # merged_dict will be used for keyword arguments for request.
        # Realise that items for record has priority over target items.
        return {**target_dict, **record_dict}

    @classmethod
    def connect(cls, target, record, session=None):
        # Performs actual request using arguments from target and record.
        kwargs = cls.create_connector_arguments(target, record)
        if session:
            return session.request(**kwargs)
        else:
            return httpx.request(**kwargs)

    def get_target(self):
        return self._target

    def get_session(self):
        return self._session

    def get_callable_session(self):
        return self._callable_session

    def close(self):
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncConnector(Connector):
    _session_type = httpx.AsyncClient

    @classmethod
    async def connect(cls, target, record, session=None):
        # Performs async request using arguments from target and record.
        kwargs = cls.create_connector_arguments(target, record)
        if session is not None:
            return await session.request(**kwargs)
        else:
            # Session need to be created manually as it was not provided.
            # That means manually calling session function if neccessary.
            async with cls._callable_session() as session:
                return await session.request(**kwargs)

    async def aclose(self):
        await self._session.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()


# AsyncConnector does not need 'close()' as it has 'aclose()'.
try:
    del AsyncConnector.close
except AttributeError:
    pass