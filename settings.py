import os
import string


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')


MAX_LONG = 1024

MAX_SHORT = 16

MIN_SHORT = 6

SYMBOLS = string.ascii_lowercase + string.ascii_uppercase + string.digits

SHORT_REGEX = rf'^[{SYMBOLS}]*$'

REPEAT_NUMBER = 5
