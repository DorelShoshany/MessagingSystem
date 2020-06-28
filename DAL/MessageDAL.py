from sqlalchemy import and_
from Config import deleteState
from application import db
from entities.Message import Message


def add_message (message):
    try:
        #db.session.execute("select * form User where name = %s" % ' ')
        db.session.add(message)
        db.session.commit()
        return True
    except IOError:
        db.session.rollback()
        return False


def get_message(message_id):
    message= Message.query.filter(and_(Message.id == message_id, Message.deleteState != deleteState.DELETED_FOR_ALL.value)).first()
    return message

