from functools import wraps


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def decorator_switcher(cls):
    cls._enable = True

    def add_switch(cls_method):
        @wraps(cls_method)
        def wrapper(ccls, arg):
            if ccls._enable:
                return cls_method(ccls, arg)
            else:
                return arg
        return wrapper

    def turn_switch(ccls, value: bool):
        ccls._enable = value

    def turn_on(ccls):
        ccls._enable = True

    def turn_off(ccls):
        ccls._enable = False

    cls.__call__ = add_switch(cls.__call__)
    cls.turn_off = turn_off
    cls.turn_on = turn_on
    cls.switch = turn_switch
    return cls
