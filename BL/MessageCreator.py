from Config import DeleteState
from Consts import FORM_NOT_FULL, MAX_LENGTHS_FOR_SUBJECT, MAX_LENGTHS_FOR_CONTENT, MIN_LENGTHS_FOR_CONTENT, \
    MIN_LENGTHS_FOR_SUBJECT, RECEIVER_NOT_EXIST
from DAL.MessageDAL import add_message
from DAL.UserDAL import get_user_from_db_by_id


class MessageCreator():

    def create(self, message, sender_id):
        self.__ensure_create_message_validation__(message)
        message.delete_state = DeleteState.NOT_DELETED.value
        message.sender_id = sender_id
        if add_message(message):
            return message.id

    def __ensure_receiver_exists__(self,receiver_id):
        receiver = get_user_from_db_by_id(receiver_id)
        if receiver is None:
            raise Exception(RECEIVER_NOT_EXIST)

    def __ensure_required_fields__(self,message):
        if "" or None or '""' in message.__dict__.values():
            raise Exception(FORM_NOT_FULL)
        if len(message.subject) > MAX_LENGTHS_FOR_SUBJECT or len(message.subject) == MIN_LENGTHS_FOR_SUBJECT:
            raise Exception("Subject should be not more than  " + str(MAX_LENGTHS_FOR_SUBJECT))
        if len(message.content) > MAX_LENGTHS_FOR_CONTENT or len(message.content) == MIN_LENGTHS_FOR_CONTENT :
            raise Exception("Content should be not more than  " + str(MAX_LENGTHS_FOR_CONTENT))

    def __ensure_create_message_validation__(self,message):
        self.__ensure_required_fields__(message)
        self.__ensure_receiver_exists__(message.receiver_id)
