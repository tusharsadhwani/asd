def singleton(cls):
    instance = None

    def get_instance(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)

        return instance

    return get_instance


@singleton
class A:
    pass


@singleton
class B:
    pass


class C:
    pass


a1 = A()
a2 = A()

print(id(a1), id(a2))

b1 = B()
b2 = B()
print(id(b1), id(b2))

c1 = C()
c2 = C()
print(id(c1), id(c2))
