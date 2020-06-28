from BL.PasswordEncryption import length_of_the_salt, hash_salt


def verify_user_password(user, enteredPassword):
    '''
    userDbPassword <-select the hashed password from database for the given user
    salt < -extract the salt part from the saved password in database
    return PasswordEncryptor.HashSalt(enteredPassword, salt) == userDbPassword
    :param user: user
    :param enteredPassword: string
    :return: boolean
    '''
    storage = user.password

    # Getting the values back out
    salt_from_storage = storage[:length_of_the_salt]  # 32 is the length of the salt
    key_from_storage = storage[length_of_the_salt:]
    enteredPassword_hash_salt = hash_salt(enteredPassword, salt_from_storage)

    return enteredPassword_hash_salt[length_of_the_salt:] == key_from_storage