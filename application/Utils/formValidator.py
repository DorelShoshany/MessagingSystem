import re

from Config import Config
from models.resultFromController import resultFromController
# TODO: delete this class
class FormValdaitor():
    def ensure_required_fields(self, form, properties):
        form_is_not_full_res = resultFromController(isSuccess=False, Message="All form fields must be filled in")
        for x in (True if field in form.keys() else False for field in properties):
            if x == False:
                return form_is_not_full_res
        if "" in form.values():
            return form_is_not_full_res
        if '""' in form.values():
            return form_is_not_full_res
        return resultFromController(isSuccess=True, Message="All form fields are filled ")

