import os
import telebot
from dotenv import load_dotenv

from db import Poll, Option, Vote, session
from polls_functions import change_name, change_anonymous, change_public, change_retract_vote, change_status, delete, \
    change_options
from texts import start_message_text, main_menu_text, create_poll_text, my_polls_text, change_name_text, poll_info_text, \
    change_options_text
from markups import main_menu, create_poll_menu, my_polls_menu, back_menu, poll_info_menu, adding_options_menu

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
    bot.clear_step_handler(call.message)
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
            text=create_poll_text(poll.id),
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
    else:
        poll_id = data[2]
        if operation == 'get':
            bot.edit_message_text(
                text=poll_info_text(poll_id, call.from_user.id),
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                parse_mode='html',
                reply_markup=poll_info_menu(poll_id, call.from_user.id),
            )
        elif operation == 'change_name':
            bot.edit_message_text(
                text=change_name_text(poll_id),
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                parse_mode='html',
                reply_markup=back_menu
            )
            bot.register_next_step_handler(call.message, change_name, bot, call.message, poll_id)
        elif operation == 'change_anonymous':
            if change_anonymous(poll_id):
                bot.edit_message_text(
                    text=create_poll_text(poll_id),
                    chat_id=call.message.chat.id,
                    message_id=call.message.id,
                    parse_mode='html',
                    reply_markup=create_poll_menu(poll_id)
                )
        elif operation == 'change_public':
            if change_public(poll_id):
                bot.edit_message_text(
                    text=create_poll_text(poll_id),
                    chat_id=call.message.chat.id,
                    message_id=call.message.id,
                    parse_mode='html',
                    reply_markup=create_poll_menu(poll_id)
                )
        elif operation == 'change_retract_vote':
            if change_retract_vote(poll_id):
                bot.edit_message_text(
                    text=create_poll_text(poll_id),
                    chat_id=call.message.chat.id,
                    message_id=call.message.id,
                    parse_mode='html',
                    reply_markup=create_poll_menu(poll_id)
                )
        elif operation == 'change_status':
            if change_status(poll_id):
                bot.edit_message_text(
                    text=poll_info_text(poll_id, call.from_user.id),
                    chat_id=call.message.chat.id,
                    message_id=call.message.id,
                    parse_mode='html',
                    reply_markup=poll_info_menu(poll_id, call.from_user.id),
                )
        elif operation == 'options_settings':
            bot.edit_message_text(
                text=create_poll_text(poll_id),
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                parse_mode='html',
                reply_markup=adding_options_menu(poll_id),
            )
        elif operation == 'cancel':
            if delete(poll_id):
                bot.edit_message_text(
                    text=main_menu_text,
                    chat_id=call.message.chat.id,
                    message_id=call.message.id,
                    parse_mode='html',
                    reply_markup=main_menu
                )
        elif operation == 'change_options':
            bot.edit_message_text(
                text=change_options_text,
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                parse_mode='html',
                reply_markup=back_menu
            )
            bot.register_next_step_handler(call.message, change_options, bot, call.message, poll_id)



bot.infinity_polling()
