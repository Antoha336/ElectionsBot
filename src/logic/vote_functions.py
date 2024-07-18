from database.database import session, Vote


def vote(user_name, user_id, option_id, poll_id, user_vote):
    if user_vote:
        session.delete(user_vote)
    session.add(Vote(
        user_name=user_name,
        user_id=user_id,
        option_id=option_id,
        poll_id=poll_id,
    ))
    session.commit()
