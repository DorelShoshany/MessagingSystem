import datetime
import enum
import os
import export


class Config(object):

    BASE_URL = 'http://127.0.0.1:5000/'  # Running on localhost
    #CORS_HEADERS = 'Content-Type'
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string"

    # DB:
    nameFileDB = "MessagingSystemDB.db"
    basedir = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(basedir, nameFileDB))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT:
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_TOKEN_LOCATION ='cookies'
    JWT_CSRF_CHECK_FORM = True
    JWT_COOKIE_CSRF_PROTECT = False
    TIME_EXPIRES_ACCESS_TOKENS_ROLE_BASIC = 2  # days
    DAYS_EXPIRES_ACCESS_TOKENS_ROLE_CHANGE_PASSWORD = 15  # minutes
    ROLE_BASIC = "basic"
    ROLE_CHANGE_PASSWORD = "change password"
    ROLE = 'roles'

    # PASSWORD:
    LENGTH_OF_THE_SALT = 32
    LENGTH_OF_THE_PASSWORD = 10
    HISTORY_OF_THE_PASSWORDS = 3
    LOGIN_LIMIT_TRYING = 3
    PASSWORD_VALIDATION_STRUCTURE = {'[0-9]': "Make sure your password has a number in it ",
                                     '[A-Z]': "Make sure your password has a capital letter in it ",
                                     '[a-z]': "Make sure your password has a lower letter case in it "
                                     }
    #DICTIONARY_ATTACK = True
    #DICTIONARY_ATTACK_FILE = 'word_list.txt'

    # consts for routes api :
    BAD_USER_NAME_OR_PASSWORD = "Bad user name or password "
    USER_IS_LOCKED_UNTIL = "User is locked until "
    PASSWORD_NOT_CORRECT = "Password not correct "
    USER_NOT_FOUND = "User not fund "
    PASSWORD_CORRECT = "Password correct "
    VERIFY_HASH_EMAIL_WITH_DATE_SUCCESS = "Success Verify your details "
    VERIFY_HASH_EMAIL_WITH_DATE_FAILED = "Failed Verify your details "
    PASSWORD_CHANGE_SUCCESS = "Password change success "
    PASSWORD_CHANGE_FAILED = "Password change failed "
    EMAIL_IS_NOT_VALID = "Email is not valid"
    EMAIL_IS_VALID = "Email is valid"
    PASSWORD_WAS_USED_IN_THE_LAST_GIVEN_OCCURRENCES = "password was used in the last given occurrences "
    MSG_FOR_ROLE_REQUIRED = "can't continue without login!"


class TypeOfSort(enum.Enum):
    DELETED = 0
    DELETED_FOR_RECEIVER = 1
    DELETED_FOR_SENDER = 2
    DELETED_FOR_ALL = 3


'''

    try:
        print("MAIL_PASSWORD:", os.environ['MAIL_PASSWORD'])
    except KeyError:
        print("Environment variable does not exist")

'''




