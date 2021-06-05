from functools import cache


@cache
def tribo_rec(n: int) -> int:
    if n < 3:
        return 1
    return tribo_rec(n-1) + tribo_rec(n-2) + tribo_rec(n-3)


def tribo_iter(n: int) -> int:
    a, b, c = 1, 1, 1
    for _ in range(n):
        a, b, c = b, c, a + b + c

    return a


for i in range(10):
    print(f'{tribo_rec(i):3} {tribo_iter(i):3}')
