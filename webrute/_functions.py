from webrute import _connector


def connector(target, record, session=None):
    '''Performs request using target and record on session'''
    return _connector.Connector.connect(target, record, session)

async def async_connector(target, record, session=None):
    '''Performs async request using target and record on session'''
    return await _connector.AsyncConnector.connect(target, record, session)


def target_reached(response):
    '''Checks if status code of response is between 2xx'''
    return response.is_success

async def async_target_reached(response):
    '''Checks if status code of response is between 2xx'''
    return response.is_success

def target_error(response):
    '''Checks if status code of response is between 4xx and 5xx'''
    return response.is_error

async def async_target_error(response):
    '''Checks if stauts code of response is 4xx and 5xx'''
    return response.is_error



def transform_record(record, method):
    '''Transforms record into format supported by connector(request)
    
    If method is 'POST' or 'PUT' then record gets put as part of 'data'
    for request. Other supported methods like 'GET', 'OPTION' or 'DELETE'
    will result in record put as part of url parameters.
    
    If record cannot be transformed then original passed record will be 
    returned. Method can mostly be retrived from target which may also 
    contain url.'''
    return _connector.Connector.transform_record(record, method)

def transform_target(target):
    '''Transforms target from 'string', 'bytes' or 'dict' into dict.
    
    if target is bytes or string then resulting target dict will have 
    its method being 'GET'. Target being 'dict' will result in original
    dict being returned unchanged.'''
    return _connector.Connector.create_target(target)

def transform_connector_arguments(connector_args):
    '''Transforms arguments of connector/request.
    
    Method if not provided will be guessed from existing arguments.
    Original connector arguments gets returned if no transformation 
    has been performed on connector arguments.'''
    return _connector.Connector.transform_connector_arguments(connector_args)

def guess_connector_method(connector_args, methods=("GET", "POST")):
    '''Guesses method to use with arguments of connector/request.'''
    return _connector.Connector.guess_connector_method(
        connector_args, methods
    )

def create_connector_arguments(target, record):
    '''Creates connector/request arguments from target and record'''
    return _connector.Connector.create_connector_arguments(target, record)


def create_session(session):
    '''Creates session(httpx.Client) from object passed as session'''
    return _connector.Connector.create_session(session)

def create_async_session(session):
    '''Creates session(httpx.AsyncClient) from object passed as session'''
    return _connector.AsyncConnector.create_session(session)


def setup_session(session):
    '''Creates session(httpx.Client) from object passed as session'''
    if session is None:
        return _connector.Connector.get_session_type()()
    return create_session(session)

def setup_async_session(session):
    '''Creates session(httpx.AsyncClient) from object passed as session'''
    if session is None:
        return _connector.AsyncConnector.get_session_type()()
    return create_async_session(session)


def session_closer(session):
    '''Closes session(httpx.AsyncClient)'''
    session.close()

async def async_session_closer(session):
    '''Closes session(httpx.AsyncClient)'''
    await session.aclose()
