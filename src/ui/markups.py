from telebot.types import InlineKeyboardMarkup as InlineMarkup, InlineKeyboardButton as InlineButton
from database.database import session, Poll, Option


def back(menu_name):
    if menu_name == 'main':
        item = InlineButton(
            text='Назад',
            callback_data='menu main'
        )
    elif menu_name == 'my_polls':
        item = InlineButton(
            text='Назад',
            callback_data='menu my_polls'
        )
    else:
        item = InlineButton(
            text='Назад',
            callback_data=f'poll get {menu_name}'
        )
    return item


def back_menu(menu_name):
    return InlineMarkup().row(back(menu_name))


main_menu = InlineMarkup()
item_1 = InlineButton(text='Создать голосование',
                      callback_data='poll create_poll')
item_2 = InlineButton(text='Мои голосования',
                      callback_data='menu my_polls')
main_menu.row(item_1).row(item_2)


def create_poll_menu(poll_id):
    item_1 = InlineButton(
        text='Изменить название',
        callback_data=f'poll change_name {poll_id}'
    )
    item_2 = InlineButton(
        text='Изменить опции',
        callback_data=f'poll change_options {poll_id}'
    )
    item_3 = InlineButton(
        text='Изменить тип голосования',
        callback_data=f'poll change_anonymous {poll_id}'
    )
    item_4 = InlineButton(
        text='Изменить видимость результатов',
        callback_data=f'poll change_public {poll_id}'
    )
    item_5 = InlineButton(
        text='Изменить возможность отмены голоса',
        callback_data=f'poll change_retract_vote {poll_id}'
    )
    item_6 = InlineButton(
        text='Отменить создание',
        callback_data=f'poll cancel {poll_id}'
    )
    item_7 = InlineButton(
        text='Подтвердить создание',
        callback_data=f'poll change_status {poll_id}'
    )
    return InlineMarkup().row(item_1, item_2).row(item_3).row(item_4).row(item_5).row(item_6, item_7).row(back('my_polls'))


def my_polls_menu(user_id):
    polls = session.query(Poll).filter(Poll.user_id == user_id)
    menu = InlineMarkup()
    for poll in polls:
        item = InlineButton(text=poll.name,
                            callback_data=f'poll get {poll.id}')
        menu.row(item)
    menu.row(back('main'))
    return menu


def poll_info_menu(poll_id, user_id):
    poll = session.query(Poll).get(poll_id)
    menu = InlineMarkup()

    if poll.status == 'Created':
        if poll.user_id == user_id:
            return create_poll_menu(poll_id)
        else:
            return back_menu('main')

    if poll.status == 'Opened':
        item_1 = InlineButton(
            text='Проголосовать',
            callback_data=f'vote {poll_id}'
        )
        item_2 = InlineButton(
            text='Ссылка для голосования',
            url=f'tg://msg_url?url=https://t.me/cw_elections_bot?start={poll_id}'
        )
        menu.row(item_1).row(item_2)

    if not poll.is_anonymous:
        item_3 = InlineButton(
            text='Подробные результаты',
            callback_data=f'poll results {poll_id}'
        )
        menu.row(item_3)

    if poll.user_id == user_id and poll.status == 'Opened':
        item_4 = InlineButton(
            text='Закончить голосование',
            callback_data=f'poll change_status {poll_id}'
        )
        menu.row(item_4)
    menu.row(back('my_polls'))

    return menu


def voting_menu(poll_id):
    options = session.query(Option).join(Poll).filter(Poll.id == poll_id)

    menu = InlineMarkup()
    for option in options:
        menu.row(InlineButton(
            text=option.name,
            callback_data=f'vote_confirm {poll_id} {option.id}'
        ))
    menu.row(back(poll_id))

    return menu
