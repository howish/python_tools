from class_structure.forking_class import forking_class


def fork_class(*args, **kwargs):
    def wrapper(cls):
        return forking_class(cls, *args, **kwargs)
    return wrapper
