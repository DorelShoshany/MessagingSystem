from sqlalchemy import and_
from Config import DeleteState
from Application import db
from DAL.entities.Message import Message


def add_message (message):
    try:
        db.session.add(message)
        db.session.commit()
        return True
    except IOError:
        db.session.rollback()
        return False


def get_message(message_id):
    message = Message.query.filter(and_(Message.id == message_id, Message.deleteState != DeleteState.DELETED_FOR_ALL.value)).first()
    return message

