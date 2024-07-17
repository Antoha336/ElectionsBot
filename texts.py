from db import session, Poll

start_message_text = "Привет! Я бот для создания всевозможных голосований.\n" \
                     "Для вызова главного меню, воспользуйтесь командой /menu"

main_menu_text = "<b>Главное меню</b>"


def create_poll_text(poll):
    return (
        f'<b>Создание голосования</b>\n\n'
        f'Название: {poll.name}\n'
        f'Голосование: {"Анонимное" if poll.is_anonymous else "Не анонимное"}\n'
        f'Результаты: {"Видно всегда" if poll.is_public else "После окончания"}\n'
        f'Отдать голос: {"Можно переголосовать" if poll.can_retract_vote else "Только один раз"}'
    )


my_polls_text = '<b>Ваши голосования</b>'


def change_name_text(poll_id):
    poll = session.query(Poll).get(poll_id)
    return (
        f'Введите новое название голосования\n'
        f'Прежнее название: <code>{poll.name}</code>'
    )
