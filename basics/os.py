import os


def create_new_file(path):
    open(path, 'w').close()


def delete_file(path):
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)


def change_ext_case(file, case='lower'):
    pre, ext = os.path.splitext(file)
    if case == 'lower':
        return pre + ext.lower()
    else:
        return pre + ext.upper()


def split_path_to_list(path):
    folders = []
    while 1:
        path, folder = os.path.split(path)
        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)
            break
    folders.reverse()
    return folders
