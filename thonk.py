import sys
from time import sleep
from typing import Generator


def get_dots() -> Generator[str, None, None]:
    while True:
        yield '.'
        yield '..'
        yield '...'


def main() -> None:
    print('Please wait, DTL is thonking', end='')
    for dots in get_dots():
        sys.stdout.write(dots)
        sys.stdout.flush()

        sleep(.6)

        dot_count = len(dots)
        sys.stdout.write('\b' * dot_count)
        sys.stdout.write(' ' * dot_count)
        sys.stdout.write('\b' * dot_count)


if __name__ == "__main__":
    main()
