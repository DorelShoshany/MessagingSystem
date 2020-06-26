import re

from Config import Config
from models.resultFromController import resultFromController


def form_is_full(form, field):
    form_is_not_full_res = resultFromController(isSuccess=False, Message="All form fields must be filled in")
    for x in (True if field in form.keys() else False for field in field):
        if x == False:
            return form_is_not_full_res
    if ""  in form.values():
        return form_is_not_full_res
    if '""'  in form.values():
        return form_is_not_full_res
    return resultFromController(isSuccess=True, Message="All form fields are filled ")


def user_is_valid(user):
    if valid_email(user.email):
        return resultFromController(isSuccess=True, Message=Config.EMAIL_IS_VALID)
    else:
        return resultFromController(isSuccess=False, Message=Config.EMAIL_IS_NOT_VALID)


def valid_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return re.search(regex, email)


def password_is_valid(password):
    if len(password) != Config.LENGTH_OF_THE_PASSWORD:
        return resultFromController(isSuccess=False, Message="Password should be exactly "+str(Config.LENGTH_OF_THE_PASSWORD)+" characters")
    for value, msg in Config.PASSWORD_VALIDATION_STRUCTURE.items():
        if re.search(value, password) is None:
            return resultFromController(isSuccess=False,
                                       Message=msg)
    return resultFromController(isSuccess=True,
                                   Message="Password is ok! ")