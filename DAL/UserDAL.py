
from application import db
from entities.User import User


def save_new_user_to_db (user):
    try:
        db.session.add(user)
        db.session.commit()
        return user
    except IOError:
        db.session.rollback()
        return None


def get_user_from_db_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_from_db_by_id(userId):
    return User.query.filter_by(id=userId).first()

