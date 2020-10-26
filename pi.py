from math import log10, sqrt
from random import random

count = 0
in_circle = 0
while True:
    x = random()
    y = random()
    distance = sqrt(x**2 + y**2)
    if distance < 1:
        in_circle += 1
    count += 1

    if log10(count) % 1 == 0:
        pi = 4 * in_circle/count
        print(f'{count}: {pi}')
