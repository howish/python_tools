from typing import NoReturn


def raise_not_implemented_error(method_name, class_name) -> NoReturn:
    raise NotImplementedError('Method {} is not implemented in class {}'
                              .format(method_name, class_name))
