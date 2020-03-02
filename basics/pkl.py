from basics import os
import pickle as pkl


def check_pkl_name(file_path):
    if not file_path.endswith('.pkl'):
        file_path += '.pkl'
    return file_path


def save_pkl(obj, file_path, show_message=True):
    file_path = check_pkl_name(file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, 'wb') as pFile:
            pkl.dump(obj, pFile)
    except Exception as e:
        if show_message:
            print('[Error][Save pkl]', e)
        return None


def load_pkl(file_path, show_message=True):
    file_path = check_pkl_name(file_path)
    try:
        if not os.path.isfile(file_path):
            return None
        with open(file_path, 'rb') as pFile:
            obj = pkl.load(pFile)
        return obj
    except Exception as e:
        if show_message:
            print('[Error][Load pkl]', e)
        return None


def load_pkl_cache(obj_name, path='pkl_cache'):
    pkl_path = os.path.join(path, obj_name + '_cache')
    return load_pkl(pkl_path)


def load_with_pkl_cache(obj_name, load_method, path='pkl_cache'):
    pkl_path = os.path.join(path, obj_name + '_cache')
    obj = load_pkl(pkl_path)
    if obj is None:
        obj = load_method()
        save_pkl(obj, pkl_path)
    return obj
