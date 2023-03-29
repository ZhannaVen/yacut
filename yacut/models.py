import random
import re
from datetime import datetime

from flask import url_for
from settings import (MAX_LONG, MAX_SHORT, MIN_SHORT, REPEAT_NUMBER,
                      SHORT_REGEX, SYMBOLS)

from yacut import db
from .exceptions import AlreadyExistsError, ValidationError, UniqueShortError

NO_URL = 'В базе данных нет записи с параметром: {}.'
SYMBOLS_NUMBER_LONG = f'Максимальная длина урла: {MAX_LONG} символов.'
INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
NAMEL_TAKEN = 'Имя "{}" уже занято.'
FAILED_ATTEMPT = 'Сервис не смог подобрать имя.'


def get_unique_short_id():
    for repeat in range(0, REPEAT_NUMBER):
        short = ''.join(random.sample(SYMBOLS, MIN_SHORT))
        if URLMap.get_url_by_short(short) is None:
            return short
    return UniqueShortError(FAILED_ATTEMPT)


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
    def get_url_by_short(short_url):
        return URLMap.query.filter_by(short=short_url).first()

    @staticmethod
    def get_or_404(short_url):
        return URLMap.query.filter_by(short=short_url).first_or_404().original

    @staticmethod
    def get_original_url(short_id):
        record = URLMap.get_url_by_short(short_id)
        if record is None:
            raise ValueError(NO_URL.format(short_id))
        return record.original

    @staticmethod
    def get_new_record(original_url, short=None, check_variables=None):
        if check_variables:
            if len(original_url) > MAX_LONG:
                raise ValidationError(SYMBOLS_NUMBER_LONG)
        if short == '' or short is None:
            short = get_unique_short_id()
        else:
            if check_variables:
                if len(short) > MAX_SHORT:
                    raise ValidationError(INVALID_SHORT)
                if not re.match(SHORT_REGEX, short):
                    raise ValidationError(INVALID_SHORT)
            if URLMap.get_url_by_short(short) is not None:
                raise AlreadyExistsError(NAMEL_TAKEN.format(short))
        record = URLMap(
            original=original_url,
            short=short,
        )
        db.session.add(record)
        db.session.commit()
        return record
