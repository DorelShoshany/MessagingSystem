from entities.User import User
from models.resultFromController import resultFromController
from services import PasswordEncryption
from services.DAL.User import save_new_user_to_db, get_user_from_db_by_email
from services.Validators import form_is_full, user_is_valid, password_is_valid


class RegistrationController():

    def register_new_user(self, request):
        register_form = request.json if request.is_json else request.form
        register_dict = dict(register_form)
        form_register_fields = ["firstName", 'lastName', 'email', 'password']
        form_valid_res = form_is_full(register_dict, form_register_fields)

        if form_valid_res.isSuccess:
            firstName = register_dict["firstName"]
            lastName = register_dict['lastName']
            email = register_dict['email']
            password = register_dict['password']

            # handle unique email in SQLAlchemy
            user = get_user_from_db_by_email(email)
            if user:
                return resultFromController(isSuccess=False, Message="User created failed. ")

            user = User(firstName=firstName, lastName=lastName, email=email, password=password)
            if user_is_valid(user).isSuccess:
                if password_is_valid(user.password).isSuccess:
                    password_encrypt = PasswordEncryption.hash_salt(password=password, salt=None)
                    user.password = password_encrypt
                    if save_new_user_to_db(user):
                        return resultFromController(isSuccess=True, Message="User created successfully. ")
                else:
                    return password_is_valid(user.password)
            else:
                return resultFromController(isSuccess=False, Message="User created failed. ")
        else:
            return form_valid_res