
from flask import request, jsonify,json
from flask_jwt_extended import jwt_required, get_jwt_identity
from BL.AccessTokenManager import AccessTokenManager
from BL.MessageCreator import MessageCreator
from BL.Modles.MessageDto import MessageDto
from BL.UserMessagesProvider import UserMessagesProvider
from Config import HttpStatusCode
from application import app
from application.controllers import convert_request_form_to_message
from application.controllers.AuthController import access_token_manager

access_token_manager = AccessTokenManager()
message_creator = MessageCreator()
user_messages_provider= UserMessagesProvider()

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
        new_message = convert_request_form_to_message(request);
        user_id = access_token_manager.get_user_id_from_identity(get_jwt_identity())
        message_id = message_creator.create(new_message, user_id)
        return jsonify({'Message Id': str(message_id)}), HttpStatusCode.OK.value
    except Exception as e:
        return str(e), HttpStatusCode.BAD_REQUEST.value


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
        #user_message_dto = user_messages.map(message = > new MessageDto(message))
       # return HttpStatus.Ok, json.dumps(user_message_dto)
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
        user_id = access_token_manager.get_user_id_from_identity(get_jwt_identity())
        receiver_unread_messages = user_messages_provider.get_unread(user_id)
        receiver_unread_messages_dto = MessageDto(many=True)
        return json.dumps(receiver_unread_messages_dto.dump(receiver_unread_messages)), HttpStatusCode.OK.value
    except Exception as e:
        return str(e), HttpStatusCode.BAD_REQUEST.value