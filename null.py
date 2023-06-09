class _Null:
    def __call__(self, *a, **kw):
        return self
    def __getattr__(self, attr):
        return self

Null = _Null()

def nullable(cls):
    def nullable_func(func):
        def wrapper(self, *a, **kw):
            ret = func(self, *a, **kw)
            if ret is None:
                return Null
            else:
                return ret
        return wrapper

    cls.__getattribute__ = nullable_func(cls.__getattribute__)
    if hasattr(cls, '__getattr__'):
        cls.__getattr__ = nullable_func(cls.__getattr__)
    else:
        cls.__getattr__ = lambda self, attr: Null

    return cls

@nullable
class Foo:
    ...

foo = Foo()

print(foo.x)
print(foo.x())
print(foo.x().y.z)
