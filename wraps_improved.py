import functools
import types


# Credit goes to https://github.com/Yelp/named_decorator
# This is a better version of functools.wraps, which changes the code
# object's `co_name` property as well, which helps differentiate between
# all the decorated functions when looking at profiling data, etc.
def better_wraps(func, decorator, **kwargs):
    def better_wraps_decorator(wrapped):
        new_name = f'{func.__name__}@{decorator.__name__}'
        code = wrapped.__code__.replace(co_name=new_name)

        new_wrapped = types.FunctionType(
            code,
            wrapped.__globals__,
            new_name,
            wrapped.__defaults__,
            wrapped.__closure__,
        )
        return functools.wraps(func, **kwargs)(new_wrapped)

    return better_wraps_decorator


def bang(func):
    @better_wraps(func, bang)
    def inner(*args, **kwargs):
        string = func(*args, **kwargs)
        return string + '!'

    return inner


@bang
def greet(name):
    return f'Hello, {name}'


print(greet('world'))
print(greet.__name__)
print(greet.__code__.co_name)
