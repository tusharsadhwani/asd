def primes_upto(n: int) -> list[int]:
    if n < 2:
        return []

    return [2] + [
        i
        for i in range(3, n + 1, 2)
        if all(
            i % 3 != 0 and i % x != 0 and i % (x + 2) != 0
            for x in range(5, int(i**0.5) + 3, 6)
        )
    ]

print(primes_upto(100))
