import random
import re
from datetime import datetime

from flask import url_for
from settings import (MAX_LONG, MAX_REPEAT, MAX_SHORT, MIN_SHORT, SHORT_REGEX,
                      SYMBOLS)

from yacut import db

MAX_LINK_LENGTH = 16
EMPTY_URL = '"url" является обязательным полем!'
CHANGE_SHORT_URL = 'Имя "{}" уже занято.'
EMPTY_ID = 'Указанный id не найден'
SHORT_URL_EXISTS = 'Имя {} уже занято!'
ERROR = 'Сервис не смог подобрать подходящее имя. Попробуйте снова.'
VALID_SHORT = 'Указано недопустимое имя для короткой ссылки'


def get_unique_short_id():
    symbols = SYMBOLS
    repeat = MAX_REPEAT
    while repeat != 0:
        short_url = ''.join(random.choice(symbols) for symbol in range(MIN_SHORT))
        repeat -= 1
        if URLMap.query.filter_by(short=short_url).first() is None:
            return short_url
        else:
            continue
    return AttributeError(ERROR)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LONG), nullable=False)
    short = db.Column(db.String(MAX_SHORT), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('index_view', _external=True) + self.short
        )

    @staticmethod
    def get_or_404(short_url):
        return URLMap.query.filter_by(short=short_url).first_or_404().original

    @staticmethod
    def get_original_url(short_id):
        url = URLMap.query.filter_by(short=short_id).first()
        if url is None:
            raise ValueError
        return url.original

    @staticmethod
    def short_url_api(original_url, short_url=None):
        if short_url == '' or short_url is None:
            short_url = get_unique_short_id()
        else:
            if URLMap.query.filter_by(short=short_url).first() is not None:
                raise NameError(short_url)
            elif not re.match(SHORT_REGEX, short_url) or len(short_url) > 16:
                raise ValueError
        url = URLMap(
            original=original_url,
            short=short_url,
        )
        db.session.add(url)
        db.session.commit()
        return url
