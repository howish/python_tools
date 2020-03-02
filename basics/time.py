import time

from decorators.decorator_prototype import Singleton


class _GlobalTimer(metaclass=Singleton):
    _dict_elapse_times = {}

    def __init__(self):
        self._dict_elapse_times['Default'] = 0.0

    @classmethod
    def tic(cls, flag_name: str = None) -> None:
        cls._dict_elapse_times[flag_name] = time.time()

    @classmethod
    def checkflag(cls, flag_name: str) -> str:
        if flag_name in cls._dict_elapse_times:
            return flag_name
        else:
            print('Not timer flag named {} is started.'.format(flag_name))
            return 'Default'

    @classmethod
    def toc(cls, flag_name: str = None) -> float:
        flag_name = cls.checkflag(flag_name)
        return time.time() - cls._dict_elapse_times[flag_name]


global_timer = _GlobalTimer()


class _TimeRecorder:
    times_record = dict()
    lastname = ''


def tic(name='last'):
    _TimeRecorder.times_record[name] = time.time()
    _TimeRecorder.lastname = name


def toc(name=None):
    if name is None:
        name = _TimeRecorder.lastname
    if name not in _TimeRecorder.times_record:
        print('[Error] timer has no name \'{}\'.'.format(name))
        return None, None
    t = time.time() - _TimeRecorder.times_record[name]
    print('[Elapse time] Block {} : {}'.format(name, t))
    return name, t


def toic(name='last'):
    res = toc()
    tic(name)
    return res


def get_time_stamp():
    return time.strftime("%Y%m%d_%H%M%S", time.gmtime())
