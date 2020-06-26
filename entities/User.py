
# data base model:
from sqlalchemy import Column, ForeignKey
from sqlalchemy import DateTime, func, ForeignKey
import uuid
from Consts import max_lengths_for_id, max_lengths_for_password, max_lengths_for_email, max_lengths_for_last_name, \
    max_lengths_for_first_name
from application import db

class User(db.Model):
    __tablename__ = 'Users'
    id = Column(db.String, name="id", primary_key=True, default= str(uuid.uuid4()))
    email = Column(db.String(max_lengths_for_email), unique=True, nullable=False)
    password = Column(db.String(max_lengths_for_password), nullable=False)
    firstName = Column(db.String(max_lengths_for_first_name), nullable=False)
    lastName = Column(db.String(max_lengths_for_last_name), nullable=False)
    creationDate = db.Column('creationDate', DateTime, default=func.now())

    def __init__(self, email, password, firstName, lastName):
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName

    def __str__(self):
        return str(self.email)
