import sys
from Consts import FORM_NOT_FULL
from DAL.entities.User import User
from DAL.entities.Message import Message

def convert_request_form_to_entity(request, properties, type_of_class):
    '''
    :param request: request
    :param properties: list of strings []
    :param type_of_class: the name of the class as a string
    :return: entity for the class
    '''

    form = __extract_form_data(request);
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

def __extract_form_data(request):
    # There was a problem with current flask version where the request.is_json was not working even though
    #    body was json and the content type was application/json. I had to use the force=True and see if it raise
    #    an exception in order to determine the body type
    try:
        form_as_json = request.get_json(force=True)
        return form_as_json
    except Exception as e:
        return request.form
