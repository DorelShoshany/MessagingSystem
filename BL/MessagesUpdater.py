from BL.UserMessagesProvider import UserMessagesProvider
from Config import deleteState
from Consts import MESSAGE_DOEST_EXISTS_OR_DOESNT_BELONG_TO_USER, BAD_REQUEST_MARK_READ
from DAL.MessageDAL import add_message
import datetime

class MessagesUpdater():
    '''
    NOT_DELETED = 0
    DELETED_FOR_RECEIVER = 1
    DELETED_FOR_SENDER = 2
    DELETED_FOR_ALL = 3
    '''
    def __init__(self):
        self.user_messages_provider = UserMessagesProvider()

    def mark_delete(self,message_id, user_id, me_only):
        message = self.user_messages_provider.get(message_id)
        is_valid_request = message is None or (message.sender_id != user_id and message.receiver_id != user_id)
        if is_valid_request:
            raise Exception(MESSAGE_DOEST_EXISTS_OR_DOESNT_BELONG_TO_USER)
        if message.receiver_id == user_id:  # user the it receiver
            if message.deleteState == deleteState.DELETED_FOR_SENDER.value:
                message.deleteState = deleteState.DELETED_FOR_ALL.value
            else:
                message.deleteState = deleteState.DELETED_FOR_RECEIVER.value

        else: # user the it sender
            if message.deleteState == deleteState.DELETED_FOR_RECEIVER.value or me_only is False: # If was deleted by receiver
                message.deleteState = deleteState.DELETED_FOR_ALL.value
            else:
                message.deleteState = deleteState.DELETED_FOR_SENDER.value
        # update message
        add_message(message)

    def mark_read(self,message_id, user_id):
        message = self.user_messages_provider.get(message_id)
        is_valid_request = message is None or message.receiver_id != user_id or message.deleteState == deleteState.DELETED_FOR_RECEIVER.value
        if is_valid_request :
            raise Exception(BAD_REQUEST_MARK_READ)
        message.lastReadDate = datetime.datetime.now()
        # update message
        add_message(message)
