from collections import deque
from typing import TypeAlias, TypeVar

T = TypeVar('T')

NestedT: TypeAlias = 'list[T | NestedT]'

def flatten(items: NestedT) -> list[T]:
    """Flatted an arbitrarily nested list, without recursion."""
    result: list[T] = []

    queue = deque(items)
    while queue:
        item = queue.popleft()
        if isinstance(item, list):
            for thing in reversed(item):
                queue.appendleft(thing)
        else:
            result.append(item)

    return result

print(flatten([[[1], 2, 3, [4, [5, 6]]], 7, [8]]))
