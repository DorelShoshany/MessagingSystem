import ast
import datetime
from flask import request, json, jsonify
from flask_jwt_extended import create_access_token


class AccessTokenManager():

    def create(self, user_id, expires=None):
        if expires is None:
            expires = datetime.timedelta(days=1)
        if user_id is None:
            raise Exception("user id not valid")
        return create_access_token(identity=json.dumps({"user": user_id}),
                                           expires_delta=expires)

    def get_user_id_from_identity(self,jwt_identity):
        dict_identity = ast.literal_eval(jwt_identity)
        return dict_identity['user']
