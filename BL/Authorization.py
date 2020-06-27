from Config import Config
from application.controllers import convert_request_to_dictionary
from models.resultFromController import resultFromController
from DAL import UserDAL
from BL.PasswordVerify import verify_user_password


class Authorization():

    def is_authorized(self, email, enteredPassword):
        user = UserDAL.get_user_from_db_by_email(email)
        if user:
            if verify_user_password(user, enteredPassword):
                return user
        return None

