import functools
from types import FunctionType


def debug_logger(func: FunctionType):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('[{}] Logging...'.format(func.__qualname__))
        print('Args: ', args)
        print('Kwargs: ', kwargs)
        result = func(*args, **kwargs)
        print('Result: ', result)
        return result
    return wrapper
