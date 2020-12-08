import os
from time import sleep


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def dots(text):
    yield text + '.'
    yield text + '..'
    yield text + '...'


def main():
    while True:
        for text in dots('Please wait\nDTL is thonking'):
            clear()
            print(text, end='')
            sleep(.6)


if __name__ == "__main__":
    main()
