from db import session, Vote


def vote(user_id, option_id, poll_id, user_vote):
    if user_vote:
        session.delete(user_vote)
    session.add(Vote(
        user_id=user_id,
        option_id=option_id,
        poll_id=poll_id,
    ))
    session.commit()
