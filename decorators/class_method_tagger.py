from types import FunctionType
from .decorator_prototype import Singleton


class _ClassMethodTagger(metaclass=Singleton):
    dict_tags = {}

    def __init__(self):
        pass

    @classmethod
    def addtags(cls, a_cls: type):
        a_cls.cmt_dict_tags = cls.dict_tags
        cls.dict_tags = {}

        def _has_tag(cself, tag: str):
            return tag in cself.cmt_dict_tags

        def _tagged_methods(cself, tag: str):
            if cself.cmt_has_tag(tag):
                return cself.cmt_dict_tags[tag]
            return {}

        def _get_method_tag(cself, func: FunctionType):
            for str_tag in cself.dict_tags:
                if func.__name__ in cself.cmt_dict_tags[str_tag]:
                    return str_tag

        a_cls.cmt_has_tag = _has_tag
        a_cls.cmt_tagged_methods = _tagged_methods
        a_cls.cmt_get_method_tag = _get_method_tag
        return a_cls

    @classmethod
    def tag(cls, str_tag: str):
        def _register(func: FunctionType):
            if str_tag not in cls.dict_tags:
                cls.dict_tags[str_tag] = {}
            cls.dict_tags[str_tag][func.__name__] = func
            return func
        return _register


class_method_tagger = _ClassMethodTagger()
