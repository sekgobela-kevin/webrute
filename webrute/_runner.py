from webrute import _connector
from webrute import _functions

import broote


def setup_runner(
    default_kwargs,
    super_, 
    target, 
    table, 
    **kwargs):
    # Setup runner by calling its super initializer with arguments.
    for dkey, dval in default_kwargs.items():
        # kwargs - Arguments to pass to runner.
        # default_kwargs - Default args to pass to 'kwargs'.
        # Adds default argument to kwargs if not already provided,
        #value = kwargs.get(dkey, None)
        if dkey not in kwargs:
            kwargs[dkey] = dval
    # Now pass target with the optional keyword arguments.
    super_.__init__(target, table, **kwargs)


def setup_connector_runner(connector_type, super_, target, table, **kwargs):
    # Setup runner using connector instance(_connector.Connector)
    session = kwargs.get("session", None)
    if issubclass(connector_type, _connector.AsyncConnector):
        connector = _functions.async_connector
        target_reached = _functions.async_target_reached
        session_closer = _functions.async_session_closer
        def callable_session():
            return _functions.setup_async_session(session)
    elif issubclass(connector_type, _connector.Connector):
        connector = _functions.connector
        target_reached = _functions.target_reached
        session_closer = _functions.session_closer
        def callable_session():
            return _functions.setup_session(session)
    default_kwargs = {
        "connector": connector,
        "target_reached": target_reached,
        "session": callable_session,
        "session_closer": session_closer
    }
    return setup_runner(default_kwargs, super_, target, table, **kwargs)

def setup_normal_runner(super_, target, table, **kwargs):
    # Setups synchronous runner instances with certain arguments.
    return setup_connector_runner(_connector.Connector, super_, target, 
    table, **kwargs)

def setup_async_runner(super_, target, table, **kwargs):
    # Setups async runner instances with certain arguments.
    return setup_connector_runner(_connector.AsyncConnector, super_, 
    target, table, **kwargs)


class runner(broote.runner):
    def __init__(self, target, table, **kwargs):
        setup_normal_runner(super(), target, table, **kwargs)

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

    passwords_field = broote.field("password", lambda: range(100))
    usernames_field = broote.field("username", ["Marry", "John", "Ben"])

    table = broote.table()
    table.add_field(passwords_field)
    table.add_primary_field(usernames_field)


    def connect(target, record):
        return "Target is '{}', record is '{}'".format(target, record)
    
    async def success(response):
        return False

    def after_connect(record, responce):
        print(record, responce.status_code)

    target = {
        "url": "http://examples.com/",
        "follow_redirects": True,
    }
    runner_ = async_runner("http://example.com/", table,
    max_success_records=1, success=success, max_multiple_primary_items=3,
    optimize=True, after_connect=after_connect, max_workers=50)
    runner_.start()
    print(runner_.get_success_records())
