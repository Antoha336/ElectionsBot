import os
import telebot
from dotenv import load_dotenv

from db import Poll, Option, Vote, session
from texts import start_message_text, main_menu_text, create_poll_text, my_polls_text
from markups import main_menu, create_poll_menu, my_polls_menu

load_dotenv()


def get_env_value(name):
    return os.environ.get(name)


bot = telebot.TeleBot(get_env_value('BOT_TOKEN'))


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id,
                     text=start_message_text)


@bot.message_handler(commands=['menu'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id,
                     text=main_menu_text,
                     parse_mode='html',
                     reply_markup=main_menu)


@bot.callback_query_handler(func=lambda call: call.data.startswith('main_menu'))
def handle(call):
    bot.edit_message_text(text=main_menu_text,
                          chat_id=call.message.chat.id,
                          message_id=call.message.id,
                          parse_mode='html',
                          reply_markup=main_menu)


@bot.callback_query_handler(func=lambda call: call.data.startswith('poll'))
def handle(call):
    data = call.data.split()
    operation = data[1]
    if operation == 'create_poll':
        poll = Poll(user_id=call.from_user.id)
        session.add(poll)
        session.commit()

        bot.edit_message_text(
            text=create_poll_text(poll),
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            parse_mode='html',
            reply_markup=create_poll_menu(poll.id)
        )
    elif operation == 'my_polls':
        bot.edit_message_text(
            text=my_polls_text,
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            parse_mode='html',
            reply_markup=my_polls_menu(call.from_user.id)
        )


bot.infinity_polling()
