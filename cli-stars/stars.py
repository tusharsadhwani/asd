"""Print Stars in your CLI"""
import argparse


def star(num):
    """Prints a six sided star of size n with alternate spacing"""
    for i in range(1, num):
        print(' '*(3*num-2-i), end='')
        print('* '*i)

    for i in range(1, num+1):
        print(' '*(i-1), end='')
        print('* '*(3*num-1-i))

    for i in range(num-1, 0, -1):
        print(' '*(i-1), end='')
        print('* '*(3*num-1-i))

    for i in range(num-1, 0, -1):
        print(' '*(3*num-2-i), end='')
        print('* '*i)


def star2(num):
    """Prints a six sided star of size n without alternate spacing"""
    for i in range(1, num):
        print(' '*(3*num-2-i), end='')
        print('*'*(2*i-1))

    for i in range(1, num+1):
        print(' '*(i-1), end='')
        print('*'*(6*num-3-2*i))

    for i in range(num-1, 0, -1):
        print(' '*(i-1), end='')
        print('*'*(6*num-3-2*i))

    for i in range(num-1, 0, -1):
        print(' '*(3*num-2-i), end='')
        print('*'*(2*i-1))


def david(num):
    """Prints the Star of David of size n"""
    for i in range(1, num):
        print(' '*(3*num-2-i), end='*')
        print(' '*(2*i-3), end='')
        print('*'*min(1, i-1))

    print('* '*((6*num-5)//2) + '*')

    for i in range(1, num):
        print(' '*(i), end='*')
        print(' '*(2*num-3-2*i), end='')
        print('*'*min(1, num-1-i), end='')
        print(' '*(2*num-3+2*i), end='*')
        print(' '*(2*num-3-2*i), end='')
        print('*'*min(1, num-1-i))

    for i in range(num-2, 0, -1):
        print(' '*(i), end='*')
        print(' '*(2*num-3-2*i), end='')
        print('*'*min(1, num-1-i), end='')
        print(' '*(2*num-3+2*i), end='*')
        print(' '*(2*num-3-2*i), end='')
        print('*'*min(1, num-1-i))

    if num > 1:
        print('* '*((6*num-5)//2) + '*')

    for i in range(num-1, 0, -1):
        print(' '*(3*num-2-i), end='*')
        print(' '*(2*i-3), end='')
        print('*'*min(1, i-1))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Print a star.')
    parser.add_argument('size', type=int, help='Size of the star')
    parser.add_argument('--david', action='store_true', help='Star of david')
    parser.add_argument('--six', action='store_true',
                        help='Six sided solid star')
    parser.add_argument('--six2', action='store_true',
                        help='Six sided solid star with alteranate fill')

    args = parser.parse_args()
    size = args.size

    if args.six:
        star(size)
    elif args.six2:
        star2(size)
    elif args.david:
        david(size)
    else:
        star(size)
