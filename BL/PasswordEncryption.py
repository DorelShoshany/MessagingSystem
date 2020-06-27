import hashlib
import os
from Config import Config

length_of_the_salt = Config.LENGTH_OF_THE_SALT


def hash_salt(password, salt):
    '''
    # Will generate salt , hash with salt and append salt in the end of the password
    # we can select some encryption that saves each password as hash of x characters and append the salt after it
    :param password: A-Z+a-z+0-9+#$%
    :param salt: 32 is the length of the salt
    :return:  salt + key
    '''
    if salt is None:
        salt = generate_new_salt()
    #password_bytes = bytes(password, encoding='utf-8')
    #salt_bytes = bytes(password, encoding='utf-8')
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # Store them as:
    storage = salt + key
    return storage


def generate_new_salt():
    return os.urandom(32)





