from configparser import ConfigParser


class IniSection:
    def __init__(self, section_dict):
        self.__dict__.update(section_dict)

    def __repr__(self):
        result = '<{} on {}>\n'.format(type(self).__name__, id(self))
        result += self.__str__()
        result += '</{} on {}>\n'.format(type(self).__name__, id(self))
        return result

    def __str__(self):
        result = ''
        for option, value in self.__dict__.items():
            result += '  {} = {}\n'.format(option, value)
        return result


class IniCont:
    def __init__(self, cont_dict):
        self.__dict__.update({section: IniSection(options)
                              for section, options in cont_dict.items()})

    def __repr__(self):
        result = '<{} on {}>\n'.format(type(self).__name__, id(self))
        result += self.__str__()
        result += '</{} on {}>\n'.format(type(self).__name__, id(self))
        return result

    def __str__(self):
        result = ''
        for section, options in self.__dict__.items():
            result += '[{}]\n'.format(section)
            result += str(options)
        return result


def _to_config_format(obj) -> None or dict:
    sections = dict()
    if type(obj) is not dict:
        return None
    for section, section_content in obj.items():
        options = dict()
        if not hasattr(section, '__str__'):
            return None
        if type(section_content) is not dict:
            return None
        for key, value in section_content.items():
            if not hasattr(key, '__str__'):
                return None
            if not hasattr(value, '__str__'):
                return None
            options[str(key)] = str(value)
        sections[str(section)] = options
    return sections


def save_ini(obj, ini_path):
    obj = _to_config_format(obj)
    if obj is None:
        return
    config = ConfigParser()
    for section, section_cont in obj.items():
        config.add_section(section)
        for key, value in section_cont.items():
            config.set(section, key, value)
    with open(ini_path, 'w') as ini_file:
        config.write(ini_file)


def load_ini(ini_path):
    config = ConfigParser()
    config.read(ini_path)
    d = {
        section: {
            key: value
            for key, value in config.items(section)
        } for section in config.sections()
    }
    return IniCont(d)


if __name__ == '__main__':
    cont = load_ini("Config.ini")
    save_ini({"A": {1: 2}, "B": {"abd": 1325}}, "out.ini")
