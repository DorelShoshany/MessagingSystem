from models.resultFromController import resultFromController

class MessageBL():

    def send (self, request):
        register_form = request.json if request.is_json else request.form
        send_dict = dict(register_form)
        form_send_fields = ["receiverId", 'subject', 'content']