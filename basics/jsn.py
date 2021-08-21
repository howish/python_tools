import os
import json as jsn
from typing import Any, Callable


def _check_jsn_path(path):
    if not path.endswith('.json'):
        path += '.json'
    return path


def save_jsn(obj, file_path):
    file_path = _check_jsn_path(file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding="utf8") as pFile:
        jsn.dump(obj, pFile, indent=4, sort_keys=True)


def load_jsn(file_path, show_message=True):
    file_path = _check_jsn_path(file_path)
    try:
        with open(file_path, 'r', encoding="utf8") as pFile:
            obj = jsn.load(pFile)
        return obj
    except Exception as e:
        if show_message:
            print('[Error][Load jsn]', e)
        return None


def load_with_jsn_cache(obj_name: str, load_method: Callable,
                        path: str = 'jsn_cache', postfix: str = '_cache',
                        ignore_cached_file: bool = False) -> Any:
    """!
    It is a one-liner function doing the following things:

    1. Check whether there is a object cache for obj_name.
    2. If there is, read and return the cached object.
    3. If there isn't, get the object by execute load_method, and then save it.
    4. Return the object.

    @param obj_name: Object name
    @param load_method: Method to load the object.
    @param path: Folder of the cache file. (default = 'jsn_cache')
    @param postfix: Postfix of cache file name. (default = '_cache')
    @param ignore_cached_file: Flag that ignore cached file, and force to load object by load_method.
    @return: The target object.
    """
    jsn_path = os.path.join(path, obj_name + postfix)
    obj = None if ignore_cached_file else load_jsn(jsn_path, show_message=False)
    if obj is None:
        save_jsn({}, jsn_path)
        obj = load_method()
        save_jsn(obj, jsn_path)
    return obj
