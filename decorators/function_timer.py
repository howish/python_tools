import time
import functools
from types import FunctionType
from .decorator_prototype import Singleton, decorator_switcher


@decorator_switcher
class _OneTimer(metaclass=Singleton):
    _title = True

    def __call__(self, func: FunctionType):
        title_prefix = '[{}]'.format(func.__qualname__) if self._title else ''
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if title_prefix:
                print('{} Start'.format(title_prefix))
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print('{} {} Elapsed time: {:.7f} secs'.format(
                title_prefix, 'End,' if title_prefix else '',
                end - start))
            return result
        return wrapper

    def notitle(self, func):
        self._title = False
        wrapper = self(func)
        self._title = True
        return wrapper


one_timer = _OneTimer()


class _CumulatedTimer(metaclass=Singleton):
    _dict_elapse_times = {}
    _check_answer = None

    def __init__(self):
        self._dict_elapse_times['Default'] = 0.0

    @classmethod
    def timeit_with_answer_checking(cls, allowed_answers: tuple):
        cls._check_answer = allowed_answers
        return cls.timeit

    @classmethod
    def timeit(cls, func: FunctionType):
        @functools.wraps(func)
        def _register(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            func_name = func.__qualname__
            if cls._check_answer is not None and result not in cls._check_answer:
                return result
            if func_name not in cls._dict_elapse_times:
                cls._dict_elapse_times[func_name] = [0, 0.0]
            cls._dict_elapse_times[func_name][0] += 1
            cls._dict_elapse_times[func_name][1] += (end - start)
            return result
        return _register

    @classmethod
    def reset(cls, func_name: str = None) -> None:
        if func_name is None:
            cls._dict_elapse_times.clear()
        else:
            func_name = cls._check_name(func_name)
            cls._dict_elapse_times[func_name][0] = 0
            cls._dict_elapse_times[func_name][1] = 0.0

    @classmethod
    def _check_name(cls, func_name: str) -> str:
        for reg_name in cls._dict_elapse_times:
            if reg_name.endswith(func_name):
                return reg_name
        else:
            print('Function {} is not registed to timer.')
            return 'Default'

    @classmethod
    def get_count(cls, func_name: str) -> int:
        func_name = cls._check_name(func_name)
        return cls._dict_elapse_times[func_name][0]

    @classmethod
    def get_time(cls, func_name: str) -> float:
        func_name = cls._check_name(func_name)
        return cls._dict_elapse_times[func_name][1]

    @classmethod
    def get_summary(cls, func_name: str) -> str:
        func_name = cls._check_name(func_name)
        count = cls._dict_elapse_times[func_name][0]
        ttime = cls._dict_elapse_times[func_name][1]
        return \
            '[{}] Tatal count: {}, Total time: {:.7f} secs, Average time: {:.7f} secs'.format(
               func_name, count, ttime, ttime / count
            )

    @classmethod
    def print_summary(cls, func_name: str) -> None:
        print(cls.get_summary(func_name))


cumulated_timer = _CumulatedTimer()
