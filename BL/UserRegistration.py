import re
from Config import Config
from Consts import MAX_LENGTHS_FOR_FIRST_NAME, MAX_LENGTHS_FOR_LAST_NAME, EMAIL_IS_NOT_VALID, EMAIL_ALREADY_EXISTS, \
    PASSWORD_SHOULD_BE_EXACTLY, FORM_NOT_FULL, MIN_LENGTHS_FOR_FIRST_NAME, MIN_LENGTHS_FOR_LAST_NAME
from BL import PasswordEncryption
from DAL.UserDAL import save_new_user_to_db, get_user_from_db_by_email


class UserRegistration():

    def register_new_user(self, new_user):
        self.__ensure_validation__(new_user)
        new_user.password = PasswordEncryption.hash_salt(password=new_user.password, salt=None)
        return save_new_user_to_db(new_user)

    def __ensure_validation__(self,new_user):
        self.__ensure_required_validtion__(new_user) # Make sure all the properties are valid
        self.__ensure_email_validation__(new_user)
        self.__ensure_valid_password__(new_user.password)


    def __ensure_required_validtion__(self, new_user):
        if "" or None or '""' in new_user.__dict__.values():
            raise Exception(FORM_NOT_FULL)
        # TODO: should be in consts?
        if len(new_user.firstName) < MIN_LENGTHS_FOR_FIRST_NAME or len(new_user.firstName) > MAX_LENGTHS_FOR_FIRST_NAME:
            raise Exception("Bad first name, first name should be between " +
                            str(MIN_LENGTHS_FOR_FIRST_NAME) + " to" + str(MAX_LENGTHS_FOR_FIRST_NAME))

        if len(new_user.lastName) < MIN_LENGTHS_FOR_LAST_NAME or len(new_user.lastName) > MAX_LENGTHS_FOR_LAST_NAME:
            raise Exception("Bad last name, last name should be between " +
                            str(MIN_LENGTHS_FOR_LAST_NAME) + " to " + str(MAX_LENGTHS_FOR_LAST_NAME))


    def __ensure_email_validation__(self, email_address):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        email_as_str = str(email_address)
        if re.search(regex, email_as_str) is None:
            match_user = get_user_from_db_by_email(email_as_str)
            if match_user is not None:
               raise Exception(EMAIL_ALREADY_EXISTS)
        else:
            raise Exception(EMAIL_IS_NOT_VALID)


    def __ensure_valid_password__(self,password):
        password = str(password)
        if len(password) != Config.LENGTH_OF_THE_PASSWORD:
            raise Exception(PASSWORD_SHOULD_BE_EXACTLY + str(
                Config.LENGTH_OF_THE_PASSWORD))

        for value, msg in Config.PASSWORD_VALIDATION_STRUCTURE.items():
            if re.search(value, password) is None:
                raise Exception(msg)
