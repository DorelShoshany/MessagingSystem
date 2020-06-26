import hashlib
import os


# Will generate salt , hash with salt and append salt in the end of the password
# we can select some encryption that saves each password as hash of x characters and append the salt after it
from Config import Config

length_of_the_salt = Config.LENGTH_OF_THE_SALT


def hash_salt(password, salt):
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


def verify_user_password(user, enteredPassword):
    '''
    userDbPassword <-select the hashed password from database for the given user
    salt < -extract the salt part from the saved password in database
    return PasswordEncryptor.HashSalt(enteredPassword, salt) == userDbPassword

    '''
    storage = user.password

    # Getting the values back out
    salt_from_storage = storage[:length_of_the_salt]  # 32 is the length of the salt
    key_from_storage = storage[length_of_the_salt:]
    enteredPassword_hash_salt = hash_salt(enteredPassword, salt_from_storage)

    return enteredPassword_hash_salt[length_of_the_salt:] == key_from_storage


