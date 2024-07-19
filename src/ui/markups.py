from telebot.types import InlineKeyboardMarkup as InlineMarkup, InlineKeyboardButton as InlineButton
from database.database import session, Poll, Option, Vote


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
item_1 = InlineButton(
    text='Создать голосование',
    callback_data='poll create_poll'
)
item_2 = InlineButton(
    text='Ваши голосования',
    callback_data='menu my_polls'
)
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
    return InlineMarkup().row(item_1, item_2).row(item_3).row(item_4).row(item_5).row(item_6, item_7).row(
        back('my_polls'))


item_1 = InlineButton(
    text='Голосования, созданные вами',
    callback_data='menu user_polls'
)
item_2 = InlineButton(
    text='Голосования, с вашим участием',
    callback_data='menu voted_polls'
)
my_polls_menu = InlineMarkup().row(item_1).row(item_2).row(back('main'))


def user_polls_menu(user_id):
    menu = InlineMarkup()
    polls = session.query(Poll.id, Poll.name).filter(Poll.user_id == user_id)
    for poll_id, poll_name in polls:
        item = InlineButton(
            text=poll_name,
            callback_data=f'poll get {poll_id}'
        )
        menu.row(item)
    menu.add(back('my_polls'))

    return menu


def voted_polls_menu(user_id):
    menu = InlineMarkup()
    polls = session.query(Poll.id, Poll.name).join(Vote).filter(Vote.user_id == user_id).distinct()
    for poll_id, poll_name in polls:
        item = InlineButton(
            text=poll_name,
            callback_data=f'poll get {poll_id}'
        )
        menu.row(item)
    menu.add(back('my_polls'))

    return menu


def poll_info_menu(poll_id, user_id):
    poll = session.get(Poll, poll_id)
    if poll is None:
        poll = session.query(Poll).filter(Poll.slug == poll_id).first()

    menu = InlineMarkup()

    if poll.status == 'Created':
        if poll.user_id == user_id:
            return create_poll_menu(poll.id)
        else:
            return back_menu('main')

    if poll.status == 'Opened':
        item_1 = InlineButton(
            text='Проголосовать',
            callback_data=f'vote {poll.id}'
        )
        item_2 = InlineButton(
            text='Ссылка для голосования',
            url=f'tg://msg_url?url=https://t.me/cw_elections_bot?start={poll.slug}'
        )
        menu.row(item_1).row(item_2)

    if not poll.is_anonymous:
        item_3 = InlineButton(
            text='Подробные результаты',
            callback_data=f'poll results {poll.id}'
        )
        menu.row(item_3)

    if poll.user_id == user_id and poll.status == 'Opened':
        item_4 = InlineButton(
            text='Закончить голосование',
            callback_data=f'poll change_status {poll.id}'
        )
        menu.row(item_4)
    menu.row(back('main'))

    return menu


def voting_menu(poll_id):
    options = session.query(Option).join(Poll).filter(Poll.id == poll_id).order_by(Option.name)

    menu = InlineMarkup()
    for option in options:
        menu.row(InlineButton(
            text=option.name,
            callback_data=f'vote_confirm {poll_id} {option.id}'
        ))
    menu.row(back(poll_id))

    return menu
