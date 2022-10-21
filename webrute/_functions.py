from webrute import _connector


def connector(target, record, session=None):
    '''Performs request using target and record on session'''
    connector = _connector.Connector(target, session)
    return connector.connect(target, record, session)

async def async_connector(target, record, session=None):
    '''Performs async request using target and record on session'''
    connector = _connector.AsyncConnector(target, session)
    return await connector.connect(target, record, session)


def target_reached(response):
    '''Checks if status code of response is between 2xx'''
    return response.is_success

async def async_target_reached(response):
    '''Checks if status code of response is between 2xx'''
    return response.is_success

# def target_error(response):
#     '''Checks if status code of response is between 4xx and 5xx'''
#     return response.is_error

# async def async_target_error(response):
#     '''Returns True if stauts code of responce is 4xx and 5xx'''
#     return response.is_error



def record_transformer(record, method=None):
    r'''Transforms record into format supported by connector(request)
    
    If format of record is supported then original record gets returned.
    If method is 'POST' or 'PUT' then record gets put as part of 'data'
    for request. Other supported methods will result in record being
    part of url parameter.
    
    Method can mostly be retrived from target which may also contain url.'''
    return _connector.Connector.transform_record(record, method)

def create_connector_arguments(target, record):
    '''Generates keyword arguments to use when making request.'''
    return _connector.Connector.create_connector_args(target, record)
