from webrute import _request
from webrute import _session

import broote


def setup_request_info(target, record):
    # Creates dict with information for creating request.
    # Target needs to be dict with request information.
    # Dynamic information about request can be found within record.
    # if isinstance(target, (str, bytes)):
    #     # Creates dict from target as its likely to be url.
    #     target = {"url": target}
    # Merges target dict with record to create new dict.
    return {**target, **record}

def setup_custom_request(target, record):
    # Creates request object fro target and record.
    request_info = setup_request_info(target, record)
    return _request.Request(**request_info)


def connect_function(target, record, session=None):
    r'''Performs request into target using information from record.

    Both target and record provide information for performing request.
    'requests' and 'aiohttp' are likely to be used for the request.'''
    custom_request = setup_custom_request(target, record)
    return _session.request(custom_request, session)

async def async_connect_funcion(target, record, session=None):
    '''Performs async request into target using information from record'''
    custom_request = setup_custom_request(target, record)
    return await _session.arequest(custom_request, session)


def target_reached(response):
    '''Returns True if staus code of responce is 200'''
    return response.is_success()

async def async_target_reached(response):
    '''Returns True if staus code of responce is 200'''
    return response.is_success()


def setup_runner(
    default_connect, 
    default_session, 
    default_target_reached,
    super_, 
    target, 
    table, 
    **kwargs):
    # Setup runner by calling its super initializer with arguments.
    connect = kwargs.get("connect", None)
    session = kwargs.get("session", None)
    session = kwargs.get("target_reached", None)
    # Setups default connect and session functions from arguments.
    # Original keyword arguments get overiden if they are None.
    if connect is None:
        kwargs["connect"] = default_connect
    if session is None:
        kwargs["session"] = default_session
    if session is None:
        kwargs["target_reached"] = default_target_reached
    
    # Target needs to be converted to dict if not already dict.
    # Target is allowed to be dict that may contain 'url', 'method', etc.
    if isinstance(target, (str, bytes)):
        # Target of string or bytes is likely to be url.
        target = {"url": target, "method":"GET"}
    elif not isinstance(target, dict):
        type_name = type(target).__name__
        err_msg = "Target needs to be one of (str, bytes, dict) " +\
            "not '{}'."
        raise ValueError(err_msg.format(type_name))

    # Passes session and connector functions into initializer.
    # Its done by calling __init__() onto super().
    super_.__init__(target, table, **kwargs)


def setup_normal_runner(super_, target, table, **kwargs):
    # Setups non async runner objects.
    # See setup_runner() function above.
    return setup_runner(connect_function, _session.create_session, 
    target_reached, super_, target, table, **kwargs)

def setup_async_runner(super_, target, table, **kwargs):
    # Setups non async runner objects.
    # See setup_runner() function above.
    async def create_session():
        return _session.create_asession()
    return setup_runner(async_connect_funcion, create_session, 
    async_target_reached, super_, target, table, **kwargs)


class basic_runner(broote.basic_runner):
    def __init__(self, target, table, **kwargs):
        setup_normal_runner(super(), target, table, **kwargs)

class thread_runner(broote.thread_runner):
    def __init__(self, target, table, **kwargs):
        setup_normal_runner(super(), target, table, **kwargs)

class async_runner(broote.async_runner):
    def __init__(self, target, table, **kwargs):
        setup_async_runner(super(), target, table, **kwargs)


if __name__ == "__main__":
    import broote

    passwords_field = broote.field("password", lambda: range(10**10))
    usernames_field = broote.field("username", ["Marry", "John", "Ben"])

    table = broote.table()
    table.add_field(passwords_field)
    table.add_primary_field(usernames_field)

    def success(response):
        # Matches Username "Ben" and Password 1
        return ("Ben" in response) and "1" in response

    def connect(target, record):
        return "Target is '{}', record is '{}'".format(target, record)

    def after(record, responce):
        print(responce)

    runner_ = basic_runner("fake target", table, 
    max_success_records=1, max_multiple_primary_items=3, success=success,
    optimize=True, after_attempt=after)
    runner_.start()
    print(runner_.get_success_records())