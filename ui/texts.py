from sqlalchemy import func
from database import session, Poll, Vote, Option

start_message_text = (
    'Привет! Я бот для создания всевозможных голосований.\n'
    'Для вызова главного меню, воспользуйтесь командой /menu'
)

main_menu_text = '<b>Главное меню</b>'


def create_poll_text(poll_id):
    poll = session.query(Poll).get(poll_id)
    options = session.query(Option).join(Poll).filter(Poll.id == poll_id)

    text = (
        f'<b>Создание голосования</b>\n\n'
        f'Название: {poll.name}\n\n'
        f'Тип голосования: {"Скрытое (Анонимное)" if poll.is_anonymous else "Открытое (Не анонимное)"}\n'
        f'Видимость результатов: {"Всегда" if poll.is_public else "После окончания"}\n'
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
    ).filter(
        Option.poll_id == poll_id
    ).group_by(
        Option.id
    ).order_by(
        Option.name
    )

    if poll.status == 'Created':
        if poll.user_id == user_id:
            return create_poll_text(poll_id)
        else:
            return 'Нет доступа к голосованию, т.к. голосование ещё не было открыто'

    text = (
        f'<b>Информация о голосовании</b>\n\n'
        f'Название: {poll.name}\n'
        f'Статус голосования: {"Проходит" if poll.status == "Opened" else "Закончено"}\n'
        f'Тип голосования: {"Скрытое (Анонимное)" if poll.is_anonymous else "Открытое (Не анонимное)"}\n'
        f'Видимость результатов: {"Всегда" if poll.is_public else "После окончания"}\n'
        f'Отмена голоса: {"Доступна" if poll.can_retract_vote else "Не доступна"}\n\n'
        f'Опции:\n'
    )

    if poll.is_public or poll.status == 'Closed':
        for option_name, vote_count in votes:
            text += f'{option_name}' + f' (количество голосов - {vote_count})\n'
    else:
        for option_name, vote_count in votes:
            text += f'{option_name}' + f' (количество голосов - ?)\n'

    text += f'\nКоличество проголосовавших: {sum([option.vote_count for option in votes])}'

    return text


change_options_text = (
    'Введите опции для голосования, вводя каждую с новой строки. Например:\n'
    'Опция №1\n'
    'Опция №2\n'
)


def voting_text(can_retract_messages, vote):
    text = '<b>Голосование</b>\n\n'
    if vote:
        text += f'Вы уже проголосовали за опцию "{vote.option.name}", но вы можете переголосовать, выбрав другую опцию'
    elif not can_retract_messages:
        text += 'В голосовании <b>не доступно</b> переголосование, то есть проголосовать можно только один раз'
    else:
        text += (
            'В голосовании <b>доступно</b> переголосование. Впоследствии вы сможете изменить свой выбор, '
            'если голосование не будет закончено'
        )

    return text


def results_text(poll_id):
    poll = session.get(Poll, poll_id)
    options = session.query(
        Option.name,
        Vote.user_name
    ).join(
        Vote, Vote.option_id == Option.id, isouter=True
    ).filter(
        Option.poll_id == poll_id
    ).order_by(
        Option.name
    )

    if poll.is_anonymous:
        return 'Нет доступа к подробным результатам голосования, т.к. голосование анонимное'
    elif not poll.is_public and poll.status != 'Closed':
        return 'Нет доступа к подробным результатам голосования, т.к. голосование не окончено'

    text = (
        f'<b>Информация о голосовании (Результаты)</b>\n\n'
        f'Название: {poll.name}\n\n'
        f'Результаты:\n'
    )

    votes = dict()
    for name, user_name in options:
        if name not in votes:
            votes[name] = set()
        if user_name is not None:
            votes[name].add(user_name)

    for option in votes:
        text += f'Опция: {option} (количество голосов - {len(votes[option])})\n'
        for user_name in votes[option]:
            text += f'-{user_name}\n'

    return text
