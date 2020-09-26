import re

with open('creeper.txt') as f:
    lyric = f.read()

words = re.compile(r'\w+')
words_list = re.findall(words, lyric)

with open('creeper.txt', 'w') as f:
    for word in words_list:
        f.write(word.lower() + '\n')