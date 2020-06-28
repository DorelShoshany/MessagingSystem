import datetime
from BL.AccessTokenManager import AccessTokenManager
from Config import Config, HttpStatusCode
from Consts import BAD_USER_NAME_OR_PASSWORD, REGISTER_SUCCEEDED, MSG_FOR_ROLE_REQUIRED, WELCOME_MESSAGE
from application import app, jwt
from flask import request, jsonify
from BL.Authorization import Authorization
from BL.UserRegistration import UserRegistration
from application.controllers import convert_request_form_to_entity, convert_request_to_dictionary

user_registration = UserRegistration()
authorization = Authorization()
access_token_manager = AccessTokenManager()

@app.route("/")
@app.route("/index")
def index():
    return WELCOME_MESSAGE


# noinspection PyBroadException
@app.route("/register", methods=['POST'])
def register():
    '''
    This will register the user and will return his user_id
    :return: user_id
    '''
    try:
        properties = ['firstName', 'lastName', 'email', 'password']
        new_user = convert_request_form_to_entity(request, properties, "User");
        user = user_registration.register_new_user(new_user)
        if user is not None:
            return jsonify({REGISTER_SUCCEEDED: user.id}), HttpStatusCode.CREATED.value
    except Exception as e: # Error handling
        return str(e), HttpStatusCode.BAD_REQUEST.value


@app.route("/login", methods=['POST'])
def login():
    '''
    This will login the user and return a self signed token with the user id
    :return: access_token_cookie
    '''
    try:
        auth_request_dict = convert_request_to_dictionary(request)
        user = authorization.is_authorized(auth_request_dict['email'], auth_request_dict['password']);
        if user is None:
            return BAD_USER_NAME_OR_PASSWORD, HttpStatusCode.UNAUTHORIZED.value
        else:
            expires = datetime.timedelta(days=Config.TIME_EXPIRES_ACCESS_TOKENS_ROLE_BASIC)
            access_token = access_token_manager.create(user.id, expires)
            resp = jsonify({'login': True})
            resp.set_cookie('access_token_cookie', access_token, expires)
            return resp, HttpStatusCode.OK.value
    except NameError:
        return HttpStatusCode.BAD_REQUEST.value


@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return jsonify(MSG_FOR_ROLE_REQUIRED),  HttpStatusCode.UNAUTHORIZED.value
