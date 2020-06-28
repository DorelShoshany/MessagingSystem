import sys
from Consts import FORM_NOT_FULL
from entities.User import User
from entities.Message import Message

# TODO change form init file name to utiils

def convert_request_form_to_entity(request, properties, type_of_class):
    '''
    :param request: request
    :param properties: list of strings []
    :param type_of_class: the name of the class as a string
    :return: entity for the class
    '''
    form = request.json if request.is_json else request.form
    form_as_dict = dict(form)
    is_valid_form(form_as_dict, properties)
    class_type = getattr(sys.modules[__name__], type_of_class)
    entity = class_type.from_json(form)
    return entity

def convert_request_to_dictionary(request):
    '''
    :param request: request
    :return: dict {}
    '''
    form = request.json if request.is_json else request.form
    entity_dict = dict(form)
    return entity_dict

def is_valid_form(request_params, properties):
    for x in (True if field in request_params.keys() else False for field in properties):
        if x is False:
            raise Exception(FORM_NOT_FULL)
    if " " in request_params.values():
        raise Exception(FORM_NOT_FULL)
    if '""' in request_params.values():
        raise Exception(FORM_NOT_FULL)