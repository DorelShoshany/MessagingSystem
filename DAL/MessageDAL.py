from Config import deleteState
from application import db
from entities import Message


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
    return Message.query.filter_by(id=message_id, deleteState=deleteState.DELETED_FOR_ALL.value is None).first()

