from db import session, Poll, Option
from texts import create_poll_text
from markups import create_poll_menu


def change_name(message, bot, call_message, poll_id):
    poll = session.query(Poll).get(poll_id)
    if poll.status == 'Opened':
        return False

    poll.name = message.text
    session.commit()
    bot.edit_message_text(
        text="Успешно!",
        chat_id=call_message.chat.id,
        message_id=call_message.id,
        parse_mode='html'
    )
    bot.send_message(
        text=create_poll_text(poll_id),
        chat_id=message.chat.id,
        parse_mode='html',
        reply_markup=create_poll_menu(poll_id)
    )


def change_anonymous(poll_id):
    poll = session.query(Poll).get(poll_id)
    if poll.status == 'Opened':
        return False

    poll.is_anonymous = not poll.is_anonymous
    session.commit()
    return True


def change_public(poll_id):
    poll = session.query(Poll).get(poll_id)
    if poll.status == 'Opened':
        return False

    poll.is_public = not poll.is_public
    session.commit()
    return True


def change_retract_vote(poll_id):
    poll = session.query(Poll).get(poll_id)
    if poll.status == 'Opened':
        return False

    poll.can_retract_vote = not poll.can_retract_vote
    session.commit()
    return True


def change_status(poll_id):
    poll = session.get(Poll, poll_id)
    options = session.query(Option).join(Poll).filter(Poll.id == poll_id).count()
    if poll.status == 'Closed':
        return False
    elif poll.status == 'Created' and options < 2:
        return None

    poll.status = 'Closed' if poll.status == 'Opened' else 'Opened'
    session.commit()
    return True


def delete(poll_id):
    poll = session.query(Poll).get(poll_id)
    if poll.status == 'Opened':
        return False

    session.delete(poll)
    session.commit()
    return True


def change_options(message, bot, call_message, poll_id):
    options = session.query(Option).join(Poll).filter(Poll.id == poll_id)
    for option in options:
        session.delete(option)

    new_options = message.text.split('\n')
    for option in new_options:
        session.add(Option(name=option, poll_id=poll_id))
    session.commit()

    bot.edit_message_text(
        text='Успешно!',
        chat_id=call_message.chat.id,
        message_id=call_message.id,
        parse_mode='html'
    )
    bot.send_message(
        text=create_poll_text(poll_id),
        chat_id=message.chat.id,
        parse_mode='html',
        reply_markup=create_poll_menu(poll_id)
    )