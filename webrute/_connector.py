from webrute._attributes import RequestAttrs
from webrute._attributes import RequestGetAttrs
from webrute._attributes import RequestPostAttrs
from webrute._attributes import SessionAttrs

import forcetable
import httpx



class Connector():
    def __init__(self, target, session=None) -> None:
        self._setup_target(target)
        self._setup_session(session)

    def _setup_target(self, target):
        # Setupstarget to ensure its in right format and type.
        # Avoid using 'self' here as method is called by initializer.
        self._target = self.create_target(target)
        
    def _setup_session(self, session):
        # Setups session either being function returnong httpx.Client
        # or httpx.Client itself.
        # Function is better a it lets 'broote' creates session itself.
        # Avoid using 'self' here as method is called by initializer.
        if session is None:
            # Better create session other than leaving it None.
            self._session = httpx.Client()
        else:
            # Session is set to function
            self._session = lambda: self.create_session(
                session, httpx.Client
            )

    
    @classmethod
    def create_session(cls, session, session_type):
        # Creates session from object that was passed as session.
        # session is whatever object that was passed as session.
        # It could be httpx.Client, dict, None, etc.
        if isinstance(session, session_type):
            return session
        else:
            # These lines are not worth it(may be removed in future).
            # Performance is wasted when creating SessionAttrs instance.
            session_attrs = SessionAttrs.to_instance(session)
            attrs_dict = session_attrs.get_attrs()
            return session_type(**attrs_dict)

    @classmethod
    def create_target(cls, target):
        # Creates target from object that was passed as target.
        # Request may be None, dict, etc.
        if isinstance(target, (str, bytes)):
            # String target will be taken as GET request.
            target = RequestGetAttrs(url=target)
        # RequestAttrs will be used when performing request.
        return RequestAttrs.to_instance(target)


    @classmethod
    def transform_record(cls, record, method):
        # Tests if 30% of record keys are compatible with request args.
        if RequestAttrs.attrs_supported(record.keys(), 0.3):
            # 30% of record keys are compatible with request arguments.
            # It may be slower than without min_ratio supplied.
            return record
        elif method in  {"POST", "PUT"}:
            return forcetable.record({"data": record})
        elif method in {"GET", "OPTION", "DELETE"}:
            return forcetable.record({"params": record})
        return record

    @classmethod
    def create_connector_args(cls, target, record):
        # Creates arguments to be used when perfoming making request.
        # Target needs to be transformed to make it compatible with request.
        target_attrs = cls.create_target(target)
        # Tries to get method from target if exists.
        method = target_attrs.get_attr("method", None)
        # Transforms record to be compatible with request methods.
        # Not guaranteed to be fully compatible(just take it as compatible)
        compatible_record = cls.transform_record(record, method)
        # Now create Attributes instance from new record.
        # This validate record to ensure its compatible with request.
        record_attrs = RequestAttrs.to_instance(compatible_record)
        # Gets dict version of Attributes objects.
        record_dict = record_attrs.get_attrs()
        target_dict = target_attrs.get_attrs()

        # merged_dict will be used for keyword arguments for request.
        # Realise that items for record has priority over target items.
        merged_dict = {**target_dict, **record_dict}
        if "method" not in merged_dict:
            # Get request is used if supported else POST is used.
            if RequestGetAttrs.attrs_supported(record.keys()):
                merged_dict["method"] = "GET"
            else:
                merged_dict["method"] = "POST"
        return merged_dict

    def connect(self, target, record, session=None):
        # Performs actual request using arguments from target and record.
        kwargs = self.create_connector_args(
            self._target, record
        )
        if session:
            return session.request(**kwargs)
        else:
            return httpx.request(**kwargs)

    def get_target(self):
        return self._target

    def get_session(self):
        return self._session


class AsyncConnector(Connector):
    def _setup_session(self, session):
        # Setups session either being function returnong httpx.AsyncClient
        # or httpx.AsyncClient itself.
        # Avoid using 'self' here as method is called by initializer.
        if session is None:
            # Better create session other than leaving it None.
            self._session = httpx.AsyncClient()
        else:
            async def create_session():
                return self.create_session(session, httpx.AsyncClient)
            # Session is set to coroutine function.
            self._session = create_session

    async def connect(self, target, record, session=None):
        # Performs async request using arguments from target and record.
        kwargs = self.create_connector_args(
            self._target, record
        )
        if session is not None:
            return await session.request(**kwargs)
        else:
            # Session need to be created manually as it was not provided.
            # That means manually calling session function if neccessary.
            if callable(self._session):
                # self._session() need to be called to get actual session.
                _session = await self._session()
            else:
                _session = self._session
            # Session is now ready to use as usual.
            async with _session as session:
                return await session.request(**kwargs)
