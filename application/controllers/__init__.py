

from entities.Message import Message
from entities.User import User

# TODO change form init file name to utiils

def convert_request_form_to_user(request):
    form = request.json if request.is_json else request.form
    firstName = form["firstName"]
    lastName = form['lastName']
    email = form['email']
    password = form['password']
    user = User(firstName=firstName, lastName=lastName, email=email, password=password)
    return user


def convert_request_to_dictionary(request, properties):
    form = request.json if request.is_json else request.form
    entity_dict = dict(form)
    return entity_dict


def convert_request_form_to_message(request):
    form = request.json if request.is_json else request.form
    receiver_id = form['receiver_id']
    subject = form['subject']
    content = form['content']
    message = Message(receiver_id=receiver_id, subject=subject, content=content)
    return message
