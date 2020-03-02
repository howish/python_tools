
def rebind(target_class, core_name, method_name):
    def wrapper(self, *args, **kwargs):
        return getattr(getattr(self, core_name), method_name)(*args, **kwargs)
    setattr(target_class, method_name, wrapper)


def forking_class(forked_class, core_name, superclass_flag_name, superclass_dict, inherited_methods):
    def _init(self, superclass_flag, *args, **kwargs):
        setattr(self, core_name, superclass_dict[superclass_flag](*args, **kwargs))
        setattr(self, superclass_flag_name, superclass_flag)

    def _getattribute(self, item: str):
        try:
            return object.__getattribute__(self, item)
        except AttributeError as e:
            try:
                return object.__getattribute__(self, core_name).__getattribute__(item)
            except AttributeError:
                raise e

    def _setattr(self, item, value):
        try:
            getattr(object.__getattribute__(self, core_name), item)
            object.__getattribute__(self, core_name).__setattr__(item, value)
        except AttributeError:
            object.__setattr__(self, item, value)

    forked_class.__init__ = _init
    forked_class.__getattribute__ = _getattribute
    forked_class.__setattr__ = _setattr

    for inherited_method in inherited_methods:
        rebind(forked_class, core_name, inherited_method)

    return forked_class


def create_forked_class(class_name, *args, **kwargs):
    forked_class = type(class_name, (), {})
    return forking_class(forked_class, *args, **kwargs)
