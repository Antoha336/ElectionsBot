from telebot.types import InlineKeyboardMarkup as InlineMarkup, InlineKeyboardButton as InlineButton
from db import session, Poll, Vote

back = InlineButton(text='Назад',
                    callback_data='main_menu')

main_menu = InlineMarkup()
item_1 = InlineButton(text='Создать голосование',
                      callback_data='poll create_poll')
item_2 = InlineButton(text='Мои голосования',
                      callback_data='poll my_polls')
main_menu.row(item_1).row(item_2)


def create_poll_menu(poll_id):
    item_1 = InlineButton(
        text='Изменить название',
        callback_data=f'poll change_name {poll_id}')
    item_2 = InlineButton(
        text='Изменить тип голосования',
        callback_data=f'poll change_anonymous {poll_id}')
    item_3 = InlineButton(
        text='Изменить видимость результатов',
        callback_data=f'poll change_public {poll_id}')
    item_4 = InlineButton(
        text='Изменить возможность отмены голоса',
        callback_data=f'poll change_retract_vote {poll_id}')
    item_5 = InlineButton(
        text='Следующий шаг (добавление вариантов голосования)',
        callback_data=f'poll next_step {poll_id}')
    item_6 = InlineButton(
        text='Отменить создание',
        callback_data=f'poll cancel {poll_id}'
    )
    return InlineMarkup().row(item_1).row(item_2).row(item_3).row(item_4).row(item_5).row(item_6)


def adding_options_menu(poll_id):
    item_1 = InlineButton(
        text='Изменить опции',
        callback_data=f'poll change_options {poll_id}'
    )
    item_2 = InlineButton(
        text='Подтвердить создание',
        callback_data=f'poll change_status {poll_id}')
    item_3 = InlineButton(
        text='Отменить создание',
        callback_data=f'poll cancel {poll_id}')
    return InlineMarkup().row(item_1).row(item_2).row(item_3)


def my_polls_menu(user_id):
    polls = session.query(Poll).filter(Poll.user_id == user_id)
    menu = InlineMarkup()
    for poll in polls:
        item = InlineButton(text=poll.name,
                            callback_data=f'poll get {poll.id}')
        menu.row(item)
    menu.row(back)
    return menu


back_menu = InlineMarkup().row(back)


def poll_info_menu(poll_id, user_id):
    poll = session.query(Poll).get(poll_id)
    has_vote = session.query(Vote).join(Poll).filter(Poll.id == poll_id and Vote.user_id == user_id).count()
    print(has_vote)

    item_1 = InlineButton(
        text='Проголосовать (Не доступно)' if has_vote else 'Проголосовать',
        callback_data=f'vote {poll_id}'
    )
    item_2 = InlineButton(
        text='Просмотреть результаты' if poll.is_public or poll.status == "Closed" else 'Результаты пока не доступны',
        callback_data=f'poll results {poll_id}'
    )
    menu = InlineMarkup().row(item_1).row(item_2)
    if poll.user_id == user_id and poll.status == 'Opened':
        item_3 = InlineButton(
            text='Закрыть голосование',
            callback_data=f'poll change_status {poll_id}'
        )
        menu.row(item_3)
    menu.row(back)

    return menu
