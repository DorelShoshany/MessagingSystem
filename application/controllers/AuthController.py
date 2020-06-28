import datetime

from BL.AccessTokenManager import AccessTokenManager
from Config import Config, HttpStatusCode
from Consts import BAD_USER_NAME_OR_PASSWORD, REGISTER_SUCCEEDED, MSG_FOR_ROLE_REQUIRED
from DAL.UserDAL import get_user_from_db_by_email
from application import app, jwt
from flask import request, json, jsonify
from BL.Authorization import Authorization
from BL.UserRegistration import UserRegistration
from application.Utils.formValidator import FormValdaitor
from application.controllers import  convert_request_form_to_user, convert_request_to_dictionary

user_registration = UserRegistration()
authorization = Authorization()
access_token_manager = AccessTokenManager()

@app.route("/")
@app.route("/index")
def index():
    return "hi"


# noinspection PyBroadException
@app.route("/register", methods=['POST'])
def register():
    try:
        new_user = convert_request_form_to_user(request);
        user_registration.register_new_user(new_user)
        return REGISTER_SUCCEEDED, HttpStatusCode.CREATED.value
    except Exception as e: # Error handling
        return str(e), HttpStatusCode.BAD_REQUEST.value


@app.route("/login", methods=['POST'])
def login():
    try:
        auth_request_dict = convert_request_to_dictionary(request)
        user = authorization.is_authorized(auth_request_dict['email'], auth_request_dict['password']);
        if user is None:
            return BAD_USER_NAME_OR_PASSWORD, HttpStatusCode.UNAUTHORIZED.value
        else:
            expires = datetime.timedelta(days=Config.TIME_EXPIRES_ACCESS_TOKENS_ROLE_BASIC)
            access_token = access_token_manager.create(user.id, expires)
            resp = jsonify({'login': True}) # TODO: Bonus - Check if necessary
            resp.set_cookie('access_token_cookie', access_token, expires)
            return resp, HttpStatusCode.OK.value
    except NameError:
        return HttpStatusCode.BAD_REQUEST.value


@jwt.unauthorized_loader
def unauthorized_callback(callback):
    # No auth header
    return jsonify(MSG_FOR_ROLE_REQUIRED),  HttpStatusCode.UNAUTHORIZED.value # redirect(app.config['BASE_URL'] + '/login', 302)
