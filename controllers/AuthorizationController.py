import datetime

from Config import Config
from models.resultFromController import resultFromController
from services.DAL import User
from services.PasswordEncryption import verify_user_password
from services.Validators import form_is_full


class AuthorizationController():
    def login(self, request):
        login_form = request.json if request.is_json else request.form
        login_dict = dict(login_form)
        login_fields = ['email','password']
        login_res= form_is_full(login_dict, login_fields)
        if login_res.isSuccess:
            return start_login_process(login_dict['email'], login_dict['password'])
        else:
            return None,login_res


def start_login_process(email, enteredPassword):
    user = User.get_user_from_db_by_email(email)
    if user:
        if verify_user_password(user, enteredPassword):
            return user, resultFromController(isSuccess=verify_user_password(user, enteredPassword), Message="User Login!")
    return None, resultFromController(isSuccess=False, Message=Config.BAD_USER_NAME_OR_PASSWORD)