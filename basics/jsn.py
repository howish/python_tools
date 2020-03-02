from basics import os
import json as jsn


def save_jsn(obj, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding="utf8") as pFile:
        jsn.dump(obj, pFile)


def load_jsn(file_path, show_message=True):
    try:
        with open(file_path, 'r', encoding="utf8") as pFile:
            obj = jsn.load(pFile)
        return obj
    except Exception as e:
        if show_message:
            print('[Error][Load jsn]', e)
        return None
