import numpy as np
import os


def check_arr_file_ext(file_path):
    if not file_path.endswith('.npy'):
        file_path += '.npy'
    return file_path


def save_arr(obj, file_path, show_message=True):
    file_path = check_arr_file_ext(file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        np.save(file_path, obj)
    except Exception as e:
        if show_message:
            print('[Error][Save array]', e)
        return None


def load_arr(file_path, show_message=True):
    file_path = check_arr_file_ext(file_path)
    try:
        if not os.path.isfile(file_path):
            return None
        obj = np.load(file_path)
        return obj
    except Exception as e:
        if show_message:
            print('[Error][Load array]', e)
        return None


def load_with_arr_cache(obj_name, load_method, path='npy_cache'):
    arr_path = os.path.join(path, obj_name + '_cache')
    obj = load_arr(arr_path)
    if obj is None:
        obj = load_method()
        save_arr(obj, arr_path)
    return obj
