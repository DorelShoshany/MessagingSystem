
from Application import ma
from marshmallow_sqlalchemy import ModelSchema

class MessageDto(ModelSchema):
    class Meta:
        fields = ('id','sender_id', 'receiver_id', 'creationDate','subject','content', 'lastReadDate')


