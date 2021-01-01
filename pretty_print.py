"""Wrap your prints with stars"""
import builtins
import sys
from contextlib import contextmanager
from typing import Any, Generator, Optional


@contextmanager
def pretty_prints() -> Generator[None, None, None]:
    """Wraps print with stars"""
    _print = builtins.print

    def fancy_print(
            *values: object,
            sep: Optional[str] = ' ',
            end: Optional[str] = '\n',
            file: Optional[Any] = sys.stdout,  # should be SupportsWrite
            flush: bool = False) -> None:
        sep = sep or ' '
        end = end or '\n'
        string = sep.join(str(value) for value in values)

        lines = string.splitlines()
        length = max(len(line) for line in lines)

        _print('*' * (length + 4))
        for line in lines:
            _print(f'* {line:{length}} *', end=end, file=file, flush=flush)
        _print('*' * (length + 4))
        _print()

    builtins.print = fancy_print

    yield

    builtins.print = _print


with pretty_prints():
    print('hello')
    print('This.\nis.\na.\ntest.')
