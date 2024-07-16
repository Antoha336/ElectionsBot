from telebot.types import InlineKeyboardMarkup as InlineMarkup, InlineKeyboardButton as InlineButton
from db import session, Poll

back = InlineButton(text='Назад',
                    callback_data='main_menu')

main_menu = InlineMarkup()
item_1 = InlineButton(text='Создать голосование',
                      callback_data='poll create_poll')
item_2 = InlineButton(text='Мои голосования',
                      callback_data='poll my_polls')
main_menu.row(item_1).row(item_2)


def create_poll_menu(poll_id):
    item_1 = InlineButton(text='Изменить название',
                          callback_data=f'poll change_name {poll_id}')
    item_2 = InlineButton(text='Изменить настройку анонимности',
                          callback_data=f'poll change_anonymous {poll_id}')
    item_3 = InlineButton(text='Изменить настройку публичности',
                          callback_data=f'poll change_public {poll_id}')
    item_4 = InlineButton(text='Изменить возможность переголосования',
                          callback_data=f'poll change_retract_vote {poll_id}')
    item_5 = InlineButton(text='Подтвердить создание',
                          callback_data=f'poll create {poll_id}')
    item_6 = InlineButton(text='Отменить создание',
                          callback_data=f'poll cancel {poll_id}')
    return InlineMarkup().row(item_1).row(item_2).row(item_3).row(item_4).row(item_5).row(item_6)


def my_polls_menu(user_id):
    polls = session.query(Poll).filter(Poll.user_id == user_id)
    menu = InlineMarkup()
    for poll in polls:
        item = InlineButton(text=poll.name,
                            callback_data=f'poll {poll.id} get')
        menu.row(item)
    menu.row(back)
    return menu
