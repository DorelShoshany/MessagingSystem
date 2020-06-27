from models.resultFromController import resultFromController
from services.Validators import form_is_full


class MessageController():

    def send (self, request):
        register_form = request.json if request.is_json else request.form
        send_dict = dict(register_form)
        form_send_fields = ["receiverId", 'subject', 'content']
        form_valid_res = form_is_full(send_dict, form_send_fields)
        if form_valid_res.isSuccess:
            receiverId = send_dict["receiverId"]
            subject = send_dict['subject']
            content = send_dict['content']

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