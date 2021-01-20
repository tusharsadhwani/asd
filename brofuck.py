"Brofuck: brainfuck but bro"
import sys
from typing import List


mapping = {
    '.': 'bro',
    ',': 'brO',
    '[': 'bRo',
    ']': 'bRO',
    '+': 'Bro',
    '-': 'BrO',
    '<': 'BRo',
    '>': 'BRO',
}


def brainfuck_to_brofuck(code: str) -> str:
    """Brainfuck to brofuck"""
    bros: List[str] = []

    for char in code:
        if char not in mapping:
            continue

        bros.append(mapping[char])

    output = ' '.join(bros)
    return output


def brofuck_to_brainfuck(code: str) -> str:
    """Brainfuck to brofuck"""
    reverse_mapping = {bro: char for char, bro in mapping.items()}

    bros = code.split()
    output = ''

    for bro in bros:
        if bro not in reverse_mapping:
            continue

        output += reverse_mapping[bro]

    return output


if __name__ == "__main__":
    print(brofuck_to_brainfuck(sys.stdin.read()))
