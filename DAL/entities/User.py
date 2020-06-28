
# data base model:
from sqlalchemy import Column, ForeignKey
from sqlalchemy import DateTime, func, ForeignKey
import uuid
from Consts import  MAX_LENGTHS_FOR_PASSWORD, MAX_LENGTHS_FOR_EMAIL, MAX_LENGTHS_FOR_LAST_NAME, MAX_LENGTHS_FOR_FIRST_NAME
from Application import db

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    #TODO: diside if the porperty is with _ or not
    __tablename__ = 'Users'
    id = Column(db.String , name="id", primary_key=True, default=generate_uuid)
    email = Column(db.String(MAX_LENGTHS_FOR_EMAIL), unique=True, nullable=False)
    password = Column(db.String(MAX_LENGTHS_FOR_PASSWORD), nullable=False)
    firstName = Column(db.String(MAX_LENGTHS_FOR_FIRST_NAME), nullable=False)
    lastName = Column(db.String(MAX_LENGTHS_FOR_LAST_NAME), nullable=False)
    creationDate = db.Column('creationDate', DateTime, default=func.now())

    def __init__(self, email, password, firstName, lastName):
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName

    def __str__(self):
        return str(self.email)

    @classmethod
    def from_json(cls, data):
        return cls(**data)