
# data base model:
import datetime
import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy import DateTime, func, ForeignKey
from Consts import MAX_LENGTHS_FOR_ID, MAX_LENGTHS_FOR_SUBJECT, MAX_LENGTHS_FOR_CONTENT
from application import db

class Message(db.Model):
    __tablename__ = 'Messages'
    id = Column(db.String, name="id", primary_key=True, default= str(uuid.uuid4()))
    sender_id = Column(db.String(MAX_LENGTHS_FOR_ID), ForeignKey("User.id"), nullable=False)
    receiver_id = Column(db.String(MAX_LENGTHS_FOR_ID), ForeignKey("User.id"), nullable=False)
    subject = Column(db.String(MAX_LENGTHS_FOR_SUBJECT), nullable=False) # SQL Injection & XSS
    creationDate = db.Column('creationDate', DateTime, default=func.now())
    content = Column(db.String(MAX_LENGTHS_FOR_CONTENT), nullable=False) # SQL Injection & XSS
    lastReadDate = Column(DateTime,  nullable=True)
    deleteState = Column(db.Integer, default=0 ) # 0 - Not Deleted(Default) , 1- Deleted for receiver, 2 - Deleted for sender, 3 - Deleted for all

    def __init__(self, sender_id, receiver_id, subject, content, lastReadDate, deleteState=0):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.subject = subject
        self.content = content
        self.lastReadDate = lastReadDate
        self.deleteState = deleteState