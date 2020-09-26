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

if __name__ == "__main__":
    while True:
        for text in dots('Please wait\nDTL is thonking'):
            clear()
            print(text, end='')
            sleep(.6)
