from sqlalchemy import func
from db import session, Poll, Vote, Option

start_message_text = "Привет! Я бот для создания всевозможных голосований.\n" \
                     "Для вызова главного меню, воспользуйтесь командой /menu"

main_menu_text = "<b>Главное меню</b>"


def create_poll_text(poll_id):
    poll = session.query(Poll).get(poll_id)
    options = session.query(Option).join(Poll).filter(Poll.id == poll_id)

    text = (
        f'<b>Создание голосования</b>\n\n'
        f'Название: {poll.name}\n\n'
        f'Тип голосования: {"Скрытое (Анонимное)" if poll.is_anonymous else "Открытое (Не анонимное)"}\n'
        f'Видимость результатов: {"Видно всегда" if poll.is_public else "После окончания голосования"}\n'
        f'Отмена голоса: {"Доступна" if poll.can_retract_vote else "Не доступна"}\n\n'
        f'Опции: '
    )
    for option in options:
        text += f'\n- {option.name}'
    if not options.first():
        text += 'Пока не добавлены'

    return text


my_polls_text = '<b>Ваши голосования</b>'


def change_name_text(poll_id):
    poll = session.query(Poll).get(poll_id)
    return (
        f'Введите новое название голосования\n'
        f'Прежнее название: <code>{poll.name}</code>'
    )


def poll_info_text(poll_id, user_id):
    poll = session.get(Poll, poll_id)
    votes = session.query(
        Option.name,
        (func.count(Vote.id)).label('vote_count')
    ).join(
        Vote, Vote.option_id == Option.id, isouter=True
    ).group_by(
        Option.id
    ).order_by(
        Option.name
    )

    if poll.status == "Created":
        if poll.user_id == user_id:
            return create_poll_text(poll_id)
        else:
            return "Нет доступа к голосованию, т.к. голосование ещё не было открыто"

    text = (
        f'<b>Информация о голосовании</b>\n\n'
        f'Название: {poll.name}\n'
        f'Статус голосования: {"Проходит" if poll.status == "Opened" else "Закончено"}\n'
        f'Тип голосования: {"Скрытое (Анонимное)" if poll.is_anonymous else "Открытое (Не анонимное)"}\n'
        f'Видимость результатов: {"Видно всегда" if poll.is_public else "После окончания голосования"}\n'
        f'Отмена голоса: {"Доступна" if poll.can_retract_vote else "Не доступна"}\n\n'
        f'Опции:\n'
    )

    if poll.is_public or poll.status == 'Closed':
        for option_name, vote_count in votes:
            text += f'{option_name}' + f' ({vote_count})\n'
    else:
        for option_name, vote_count in votes:
            text += f'{option_name}' + f' (?)\n'

    text += f'\nКоличество проголосовавших: {sum([option.vote_count for option in votes])}'

    return text


change_options_text = (
    'Введите опции для голосования, каждую с новой строки. Например:\n'
    'Опция №1\n'
    'Опция №2\n'
)


def voting_text(can_retract_messages):
    return (
        '<b>Голосование</b>\n\n'
        'Обратите внимание - проголосовать можно только один раз' if not can_retract_messages else 'Доступна отмена голоса'
    )
