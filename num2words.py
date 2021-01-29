"""Numbers to words"""


def word_under_twenty(num: int) -> str:
    """Returns words for numbers upto 19"""
    words = {
        0: 'zero',
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight',
        9: 'nine',
        10: 'ten',
        11: 'eleven',
        12: 'twelve',
        13: 'thirteen',
        15: 'fifteen'
    }
    if num in words:
        return words[num]

    return words[num - 10] + 'teen'


def word_under_hundred(num: int) -> str:
    """Returns words for numbers upto 99"""
    if num < 20:
        return word_under_twenty(num)

    words = {
        2: 'twenty',
        3: 'thirty',
        4: 'forty',
        5: 'fifty',
        6: 'sixty',
        7: 'seventy',
        8: 'eighty',
        9: 'ninety',
    }

    word = words[num // 10]
    if num % 10 > 0:
        word += ' ' + word_under_twenty(num % 10)

    return word


def word_under_thousand(num: int) -> str:
    """Returns words for numbers upto 999"""
    if num < 100:
        return word_under_hundred(num)

    word = word_under_twenty(num // 100) + ' hundred'

    if num % 100 > 0:
        word += ' and ' + word_under_hundred(num % 100)

    return word


def num_to_word(num: int) -> str:
    """Convert any number to words"""
    if num < 1000:
        return word_under_thousand(num)

    starting_num = num
    while starting_num >= 1000:
        starting_num //= 1000

    multiplier = 1
    while multiplier <= num:
        multiplier *= 1000
    multiplier //= 1000

    rest_num = num - (starting_num * multiplier)

    place_map = {
        1_000: 'thousand',
        1_000_000: 'million',
        1_000_000_000: 'billion',
        1_000_000_000_000: 'trillion',
        1_000_000_000_000_000: 'quadrillion',
        1_000_000_000_000_000_000: 'quintillion',
    }

    word = f'{word_under_thousand(starting_num)} {place_map[multiplier]}'

    if rest_num > 0:
        word += ' ' + num_to_word(rest_num)

    return word


print(num_to_word(0))
print(num_to_word(1))
print(num_to_word(5))
print(num_to_word(10))
print(num_to_word(15))
print(num_to_word(30))
print(num_to_word(79))
print(num_to_word(100))
print(num_to_word(129))
print(num_to_word(536))
print(num_to_word(1000))
print(num_to_word(1527))
print(num_to_word(3780))
print(num_to_word(10000))
print(num_to_word(69420))
print(num_to_word(133700))
print(num_to_word(5291425))
print(num_to_word(824763294))
print(num_to_word(4198462836))
print(num_to_word(284974617461286412))
