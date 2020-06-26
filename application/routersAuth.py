import datetime
from flask_jwt_extended import create_access_token, set_access_cookies
from Config import Config
from application import app
from flask import request, json, jsonify
from controllers.AuthorizationController import AuthorizationController
from controllers.RegistrationController import RegistrationController


@app.route("/")
@app.route("/index")
def index():
    return "hi"


@app.route("/register", methods=['POST'])
def api_register():
    registration_controller = RegistrationController()
    res = registration_controller.register_new_user(request)
    if res.isSuccess:
        return jsonify(res.Message), 201
    else:
        resp = jsonify(res.Message)
        return resp, 400


@app.route("/login", methods=['POST'])
def login():
    authorization_controller = AuthorizationController()
    user, authorizationResult = authorization_controller.login(request)
    if authorizationResult.isSuccess:
        expires = datetime.timedelta(days=Config.TIME_EXPIRES_ACCESS_TOKENS_ROLE_BASIC)
        access_token = create_access_token(identity=json.dumps({"user": user.id}),
                                           expires_delta=expires)
        resp = jsonify({'login': True})
        resp.set_cookie('access_token', access_token, expires)
        #set_access_cookies(resp, access_token)
        return resp, 200
    else:
        return jsonify(authorizationResult.Message), 404