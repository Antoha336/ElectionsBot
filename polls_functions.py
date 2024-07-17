from db import session, Poll
from texts import create_poll_text
from markups import create_poll_menu


def change_name(message, bot, call_message, poll_id):
    poll = session.query(Poll).get(poll_id)
    poll.name = message.text
    session.commit()
    bot.edit_message_text(text="Успешно!",
                          chat_id=call_message.chat.id,
                          message_id=call_message.id,
                          parse_mode='html')
    bot.send_message(text=create_poll_text(poll),
                     chat_id=message.chat.id,
                     parse_mode='html',
                     reply_markup=create_poll_menu(poll_id))
