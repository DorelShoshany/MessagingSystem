import types

from flask import request, jsonify,json
from flask_jwt_extended import jwt_required, get_jwt_identity
from BL.AccessTokenManager import AccessTokenManager
from BL.MessageCreator import MessageCreator
from BL.MessagesUpdater import MessagesUpdater
from BL.Modles.MessageDto import MessageDto
from BL.UserMessagesProvider import UserMessagesProvider
from Config import HttpStatusCode
from Consts import MY_ONLY_SHOULD_BE_BOOLEAN, MESSAGE_SUCCESSFULLY_DELETED
from application import app
from application.controllers import convert_request_to_dictionary, is_valid_form, \
    convert_request_form_to_entity
from application.controllers.AuthController import access_token_manager

# init once
access_token_manager = AccessTokenManager()
message_creator = MessageCreator()
user_messages_provider = UserMessagesProvider()
messages_updater = MessagesUpdater()


@app.route("/get", methods=["GET"])
@jwt_required
def get():
    '''
     will return all not deleted* messages where the user is the sender or the receiver order by createdDate asec
    it is also possible to return the result as a tuple of {sendMessages: Message[], receivedMessages: Message[]}
    but since the client can always easily do I returned it as a flat array
    *not deleted messages for recipient are messages where the deleteState equal to  0,2
    *not deleted messages for sender are message where the deleteState equal 0,1
    :return: all not deleted messages
    '''
    try:
        user_id = access_token_manager.get_user_id_from_identity(get_jwt_identity())
        user_messages = user_messages_provider.get_all_messages_user(user_id)
        user_messages_dto = MessageDto(many=True)
        return json.dumps(user_messages_dto.dump(user_messages)), HttpStatusCode.OK.value
    except Exception as e:
        return str(e), HttpStatusCode.BAD_REQUEST.value


@app.route("/unread", methods=["GET"])
@jwt_required
def unread():
    '''
    will return all unread and not deleted messages where the user is the receiver order by created date asc
    *not deleted messages for receiver are message where the deleteState doesn't equal 1 or 3
    :return: all unread and not deleted messages
    '''
    try:
        #TODO order by crated date
        user_id = access_token_manager.get_user_id_from_identity(get_jwt_identity())
        receiver_unread_messages = user_messages_provider.get_unread(user_id)
        receiver_unread_messages_dto = MessageDto(many=True)
        return json.dumps(receiver_unread_messages_dto.dump(receiver_unread_messages)), HttpStatusCode.OK.value
    except Exception as e:
        return str(e), HttpStatusCode.BAD_REQUEST.value


@app.route("/read", methods=["POST"]) # The reason I didn't use PUT it because this route is more for getting the message than marking it as read
@jwt_required
def read():
    '''
    This will search for an not deleted message where the id = give id
    if message doesn't exist or deletes return 404 ("message doesn't exists")
    if message does exists and the logged user is not the the recipeint id return 401(Not authrozied)
    if message was already read , the new lastReadDate will be updated with the current date
    return the message to the client
    :return: message
    '''
    try:
        request_params = convert_request_to_dictionary(request)
        properties = ["message_id"]
        is_valid_form(request_params, properties)
        message_id = request_params[properties[0]]
        user_id = access_token_manager.get_user_id_from_identity(get_jwt_identity())
        messages_updater.mark_read(message_id, user_id)
        user_message = user_messages_provider.get(message_id) # We don't need to check this result since mark_read already did the valdaition and will throw error when there is a error
        user_message_dto = MessageDto()
        return json.dumps(user_message_dto.dump(user_message)), HttpStatusCode.OK.value
    except Exception as e:
        return str(e), HttpStatusCode.BAD_REQUEST.value


@app.route("/send", methods=["POST"])
@jwt_required
def send():
    '''
    This will create a message and return the new message id  as a response
    The sender id will be taken from the access token
    The reason I didn't use an email for the receiver address is because I assume this is part of an application
    where the user can select which user he want to send and the client has the receiver id
     (Lets assume its being implemented by other service)
    :return: String message id
    '''
    try:
        properties = ['receiver_id', 'subject', 'content']
        new_message = convert_request_form_to_entity(request, properties, "Message")
        user_id = access_token_manager.get_user_id_from_identity(get_jwt_identity())
        message_id = message_creator.create(new_message, user_id)
        return jsonify({'Message Id': str(message_id)}), HttpStatusCode.OK.value
    except Exception as e:
        return str(e), HttpStatusCode.BAD_REQUEST.value


@app.route("/delete", methods=["POST"])
@jwt_required
def delete():
    '''
    This will search for a message where message id = id and deleteState != 3
     '''
    try:
        request_params = convert_request_to_dictionary(request)
        properties = ["message_id", "me_only"]
        is_valid_form(request_params, properties)
        message_id = request_params[properties[0]]
        me_only = json.loads(request_params[properties[1]])
        if isinstance(me_only, bool) is False:
            raise TypeError(MY_ONLY_SHOULD_BE_BOOLEAN)

        user_id = access_token_manager.get_user_id_from_identity(get_jwt_identity())
        # we don't need to check this result since mark_read already did the validation
        # and will throw error when there is a error
        messages_updater.mark_delete(message_id, user_id, me_only)
        return MESSAGE_SUCCESSFULLY_DELETED, HttpStatusCode.OK.value
    except Exception as e:
        return str(e), HttpStatusCode.BAD_REQUEST.value