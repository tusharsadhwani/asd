import logging

from functools import partial
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

verified_users_waitlist = set()

def check_not_bot(member, chatid, msgid, msgtext, bot, job):
    print(f'Verifying user {member.full_name}... ', end='')
    if member.id in verified_users_waitlist:
        print('Verified!')
        verified_users_waitlist.remove(member.id)
    else:
        print('Not found! kicking...')
        try:
            bot.kick_chat_member(chatid, member.id)
        except:
            pass

        try:
            bot.edit_message_text(msgtext + "\n\nUser kicked.", chat_id=chatid, message_id=msgid)
        except:
            pass


def welcome(bot, update, job_queue):
    if not update.message or not update.message.new_chat_members:
        return

    if update.message.from_user.is_bot:
        return

    for member in update.message.new_chat_members:
        if member.is_bot:
            continue

        print(f'User {member.full_name} added')

        not_bot_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(
                "I'm not a bot",
                callback_data='\n'.join([
                    str(member.id),
                    member.first_name,
                    str(update.message.chat_id),
                    str(update.message.message_id)
                ])
            )]]
        )

        sent_msg = update.message.reply_text("Welcome, new user!", reply_markup=not_bot_markup)

        job_queue.run_once(
            partial(check_not_bot, member, sent_msg.chat_id, sent_msg.message_id, sent_msg.text),
            200,
            name="idk"
        )


def not_bot_callback(bot, update):
    member_id, member_name, chatid, msgid = update.callback_query.data.split('\n')

    member_id = int(member_id)
    chatid = int(chatid)
    msgid = int(msgid)

    if update.callback_query.from_user.id != member_id:
        return

    print(f"Adding {member_name} to verified list")
    verified_users_waitlist.add(member_id)

    sent_msg = update.callback_query.message

    try:
        bot.edit_message_text(
            sent_msg.text + "\n\nUser verified.",
            chat_id=chatid,
            message_id=sent_msg.message_id
        )
    except:
        pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    updater = Updater(token='TOKEN')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CallbackQueryHandler(not_bot_callback))
    dispatcher.add_handler(MessageHandler(Filters.all, welcome, pass_job_queue=True))

    updater.start_polling()
