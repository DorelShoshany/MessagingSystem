import ast
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from application import app


def get_user_id_from_identity(jwt_identity):
    dict_identity = ast.literal_eval(jwt_identity)
    return dict_identity['user']


@app.route("/send", methods=["POST"])
@jwt_required
def send_msg():
    '''
        //  This will create a message and return the new message id  as a response
        //  The sender id will be taken from the access token
        //  The reason I didn't use an email for the receiver address is because I assume this is part of an application
                where the user can select which user he want to send and the client has the receiver id
                (Lets assume its being implemented by other service)
    :return: String message id
    '''
    user_id = get_user_id_from_identity(get_jwt_identity())
    #if packagesSectorController.add_purchase_to_user(user_id=user_id, request=request):
     #   return jsonify("Buy package success. "), 200
    #else:
    return jsonify("Send msg failed. "), 400