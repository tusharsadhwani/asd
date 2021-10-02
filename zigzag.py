"""
Problem statement:
- zigzag(5, 20) should print:

1              9              17
  2          8  10          16  18
    3      7      11      15      19
      4  6          12  14          20
        5              13

Patterns to note:

For zigzag(x, y):
- The number of lines comes from the first number `x`
- On the first line there's 14 spaces, same on the last one.
  This comes from 4x-6 spaces, as every level adds 4 spaces, but the 2nd level starts with just 2.
- The number of spaces on every middle line alternates:
  - In the 2nd line there's 2 space in the beginning, then 10, then 2, then 10...
    In the 3rd line there's 4 space in the beginning, then 6, then 4, then 6...
    i.e. 4i-2 spaces followed by 4*(x-i)-6 spaces, considering i is in range 0 to x-1
- The numbers on a line starts with i+1
- Every next number on the edge lines is + 2*(x-1)
- Every next number in the middle lines alternates between + 2*(x-i-1) and + 2*i
"""


def zigzag(lines: int, limit: int) -> None:
    """Prints a zigzag pattern."""
    if lines < 2:
        raise ValueError("lines must be >= 2")

    number = 1
    print(number, end="")
    while True:
        number += 2 * (lines - 1)
        if number > limit:
            break

        spaces = 4 * lines - 6
        print(" " * spaces, end="")
        print(number, end="")
    print()

    # ====================================

    for index in range(1, lines - 1):
        number = index + 1
        spaces = 2 * index
        print(" " * spaces, end="")

        while True:
            print(number, end="")

            spaces = 4 * (lines - index) - 6
            print(" " * spaces, end="")

            number += 2 * (lines - index - 1)
            if number > limit:
                break

            print(number, end="")
            spaces = 4 * index - 2
            print(" " * spaces, end="")

            number += 2 * index
            if number > limit:
                break
        print()

    print(" " * (2 * (lines - 1)), end="")
    number = lines
    print(number, end="")
    while True:
        number += 2 * (lines - 1)
        if number > limit:
            break

        spaces = 4 * lines - 6
        print(" " * spaces, end="")
        print(number, end="")
    print()


zigzag(5, 45)
