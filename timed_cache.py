import time

from collections import deque
from functools import wraps
from threading import Timer


def timed_cache(wrapped):
    cache_queue = deque()
    functions = {}

    def remove_cache(function):
        if functions.get(function):
            functions.pop(function)

    @wraps(wrapped)
    def func(*args, **kwargs):
        if wrapped in functions:
            return functions[wrapped]

        Timer(10, lambda: remove_cache(wrapped)).start()
        result = wrapped(*args, **kwargs)
        functions[wrapped] = result
        return result

    return func


@timed_cache
def f1():
    print('running f1')
    return 1


@timed_cache
def f2():
    print('running f2')
    return 2


@timed_cache
def f3():
    print('running f3')
    return 3
