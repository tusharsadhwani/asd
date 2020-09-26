from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import logging
import re

CREEPER = False
LYRICS = []
INDEX = 0

SLANGS = {
    'nite': 'night',
    'tonite': 'tonight',
    'cuz': 'cause',
    'cus': 'cause'
}

def load_lyrics():
    global LYRICS
    with open('creeper.txt') as f:
        LYRICS.extend(f.read().strip().split())


def same_word(in_word, lyric):
    # index pointer for input word
    iidx = 0
    # index pointer for lyric word
    lidx = 0

    # Loop runs till either the input string ends 
    # or the characters don't match
    while iidx < len(in_word) and lidx < len(lyric) and in_word[iidx] == lyric[lidx]:
        if iidx+1 < len(in_word) and in_word[iidx] != in_word[iidx+1]:
            lidx += 1
        elif lidx+1 < len(lyric) and lyric[lidx] == lyric[lidx+1]:
            lidx += 1
        iidx += 1
    
    return iidx==len(in_word) and lidx == len(lyric)-1


def words_match(word, offset):
    global LYRICS
    global INDEX

    if INDEX+offset >= len(LYRICS):
        return False

    lyric_word = LYRICS[INDEX+offset]
    return same_word(word, lyric_word)


def check_followup(text):
    global INDEX

    words = re.findall(r'\w+', text.lower().replace("'", ''))

    for i, word in enumerate(words):
        for slang_word in SLANGS:
            if same_word(word, slang_word):
                word = SLANGS[slang_word]
        
        if not words_match(word, i):
            return False
    
    INDEX += len(words)
    return True

def message_callback(bot, update):
    if update.message.chat_id > 0: return
    if not update.message.text:
        return

    global CREEPER
    global INDEX
    
    if not CREEPER:
        return
    
    msg = update.message
    text = msg.text
    following = check_followup(text)

    if not following:
        msg.delete()
    
    if INDEX == len(LYRICS):
        CREEPER = False
        msg.reply_text("We did it bois!")


def creeper(bot, update):
    msg = update.message
    if msg.chat_id > 0: return
    global CREEPER
    global INDEX

    if not CREEPER:
        CREEPER = True
        INDEX = 1
        msg.reply_text('CREEPER')
    else:
        msg.delete()

def stop(bot, update):
    if update.message.chat_id > 0: return
    global CREEPER

    CREEPER = False
    update.message.reply_text('aww man :(')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    load_lyrics()
    
    updater = Updater(token="TOKEN")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('creeper', creeper))
    dispatcher.add_handler(CommandHandler('stop', stop))
    dispatcher.add_handler(MessageHandler(Filters.all, message_callback))

    updater.start_polling()
    updater.idle()
