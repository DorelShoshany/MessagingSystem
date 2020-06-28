from Config import deleteState
from sqlalchemy import or_
from sqlalchemy import and_
from DAL.MessageDAL import get_message
from entities.Message import Message


class UserMessagesProvider():

    def get(self, message_id):
        '''
        :param message_id: string
        :return: message object orm
        '''
        return get_message(message_id)

    def get_all_messages_user(self, user_id):
        '''
        NOT_DELETED = 0
        DELETED_FOR_RECEIVER = 1
        DELETED_FOR_SENDER = 2
        DELETED_FOR_ALL = 3
        :param user_id: string
        :return: message[] object orm
        '''
        not_deleted_messages_user = Message.query.filter(
            and_(Message.deleteState != deleteState.DELETED_FOR_ALL.value,
                or_(
                and_(Message.sender_id == user_id, Message.deleteState != deleteState.DELETED_FOR_SENDER.value),
                and_(Message.receiver_id == user_id, Message.deleteState != deleteState.DELETED_FOR_RECEIVER.value))))
        return not_deleted_messages_user

    def get_unread(self, user_id):
        '''
        :return: message[] object orm
        '''
        unread_receiver_message = Message.query.filter(
            and_(Message.receiver_id == user_id,
                 Message.deleteState != deleteState.DELETED_FOR_ALL.value,
                 Message.deleteState != deleteState.DELETED_FOR_RECEIVER.value, Message.lastReadDate == None))

        return unread_receiver_message
