from webrute import _runner


def create_runner(target, table, **kwargs):
    '''Creates runner object'''
    return _runner.basic_runner(target, table, **kwargs)

def create_basic_runner(target, table, **kwargs):
    '''Creates synchronous, non conccurrent runner'''
    return _runner.basic_runner(target, table, **kwargs)

def create_thread_runner(target, table, **kwargs):
    '''Creates concurrent runner based on threads'''
    return _runner.thread_runner(target, table, **kwargs)

def create_async_runner(target, table, **kwargs):
    '''Creates concurrent runner that is asynchronous(asyncio)'''
    return _runner.async_runner(target, table, **kwargs)
