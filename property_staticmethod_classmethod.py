########################################################################
########################## Part 1 - @property ##########################
########################################################################


class C:
    def __init__(self) -> None:
        self._x = 42

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_value):
        if new_value < self._x:
            raise ValueError("x must be set to a value bigger than old one")

        self._x = new_value


c = C()
print(c.x)
c.x += 1
print(c.x)

########################################################################


class my_property:
    def __init__(self, getter_func):
        self.getter_func = getter_func
        self.setter_func = None

    def __get__(self, obj, cls):
        return self.getter_func(obj)

    def setter(self, setter_func):
        self.setter_func = setter_func

    def __set__(self, obj, value):
        self.setter_func(obj, value)


class C:
    def __init__(self) -> None:
        self._x = 42

    @my_property
    def x(self):
        return self._x

    @x.setter
    def set_x(self, new_value):
        if new_value < self._x:
            raise ValueError("new value must be bigger than old one")

        self._x = new_value


c = C()
print(c.x)
c.x += 1
print(c.x)

########################################################################


class my_property:
    def __init__(self, getter_func, setter_func=None):
        self.getter_func = getter_func
        self.setter_func = setter_func

    def __get__(self, obj, cls):
        return self.getter_func(obj)

    def setter(self, setter_func):
        return my_property(self.getter_func, setter_func)

    def __set__(self, obj, value):
        return self.setter_func(obj, value)


class C:
    def __init__(self) -> None:
        self._x = 42

    @my_property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_value):
        if new_value < self._x:
            raise ValueError("new value must be bigger than old one")

        self._x = new_value


c = C()
print(c.x)
c.x += 1
print(c.x)

########################################################################
######################## Part 2 - @staticmethod ########################
########################################################################


class C:
    @staticmethod
    def foo():
        print("foo")


C.foo()
c = C()
c.foo()

########################################################################


def my_staticmethod(func):
    def wrapper(_=None):
        return func()

    return wrapper


class C:
    @my_staticmethod
    def foo():
        print("foo")


C.foo()
c = C()
c.foo()

########################################################################


class my_staticmethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls):
        return self.func


class C:
    @my_staticmethod
    def foo():
        print("foo")


C.foo()
c = C()
c.foo()

########################################################################
######################## Part 3 - @classmethod #########################
########################################################################


class C:
    @classmethod
    def foo(cls):
        print(cls.__name__)


C.foo()
c = C()
c.foo()

########################################################################

from functools import partial


class my_classmethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls):
        return partial(self.func, cls)
        # or:
        # return lambda: self.func(cls)


class C:
    @my_classmethod
    def foo(cls):
        print(cls.__name__)


C.foo()
c = C()
c.foo()
