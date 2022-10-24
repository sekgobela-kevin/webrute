try:
    # Not all versions of broote have 'exceptions' module.
    from prodius.exceptions import *
except ImportError:
    pass


class UnsupportedAttribute(Exception):
    '''Attribute provided is not supported'''
    pass

class AttributeNotFound(Exception):
    '''Attribute provided is not supported'''
    pass