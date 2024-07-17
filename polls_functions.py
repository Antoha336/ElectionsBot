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
    bot.send_message(text=create_poll_text(poll_id),
                     chat_id=message.chat.id,
                     parse_mode='html',
                     reply_markup=create_poll_menu(poll_id))


def change_anonymous(poll_id):
    poll = session.query(Poll).get(poll_id)
    poll.is_anonymous = not poll.is_anonymous
    session.commit()


def change_public(poll_id):
    poll = session.query(Poll).get(poll_id)
    poll.is_public = not poll.is_public
    session.commit()


def change_retract_vote(poll_id):
    poll = session.query(Poll).get(poll_id)
    poll.can_retract_vote = not poll.can_retract_vote
    session.commit()
