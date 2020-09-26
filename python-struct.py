class struct:
    def __init__(self, *args):
        self.attrs = args

    def __getitem__(self, item):
        return self.__dict__.get(item)

    def __call__(self, d=None, **kw):
        a = struct(self.attrs)
        if d:
            if not isinstance(d, dict):
                raise ValueError(
                    'Initialise struct with a dictionary or named arguments')
            a.__dict__.update(d)
        else:
            a.__dict__.update(kw)
        return a

if __name__ == "__main__":
    person = struct(
        'name',
        'age'
    )

    p1 = person(
        name = "tushar",
        age = 19
    )
    p2 = person({
        'name': "udit",
        'age': 17
    })

    print(p1.name)
    print(p2.age)
