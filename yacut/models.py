import random
import re
import string
from datetime import datetime
from http import HTTPStatus

from flask import flash, render_template, url_for

from yacut import db

from .error_handlers import InvalidAPIUsage

MAX_1 = 1024
MAX_2 = 16
MAX_LINK_LENGTH = 16
LINK_LENGTH = 6
EMPTY_URL = '"url" является обязательным полем!'
CHANGE_SHORT_URL = 'Имя "{}" уже занято.'
SHORT_REGEX = r'^[A-Za-z0-9]{1,16}$'
EMPTY_ID = 'Указанный id не найден'
SHORT_URL_EXISTS = 'Имя {} уже занято!'
ERROR = 'Сервис не смог подобрать подходящее имя. Попробуйте снова.'
VALID_SHORT = 'Указано недопустимое имя для короткой ссылки'


def get_unique_short_id():
    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    short_url = ''.join(random.choice(symbols) for symbol in range(LINK_LENGTH))
    for repeat in range(MAX_2):
        if URLMap.query.filter_by(short=short_url).first():
            return get_unique_short_id()
        return short_url
    else:
        raise RecursionError('ERROR')


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_1), nullable=False)
    short = db.Column(db.String(MAX_2), unique=True)
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
            raise InvalidAPIUsage(EMPTY_ID, HTTPStatus.NOT_FOUND)
        return url.original

    @staticmethod
    def adding_into_db(original_url, short_url):
        url = URLMap(
            original=original_url,
            short=short_url,
        )
        db.session.add(url)
        db.session.commit()
        return url


    @staticmethod
    def short_url_api(data):
        if 'url' not in data:
            raise InvalidAPIUsage(EMPTY_URL)
        if 'custom_id' in data:
            custom_id = data.get('custom_id')
            if URLMap.query.filter_by(short=custom_id).first() is not None:
                raise InvalidAPIUsage(CHANGE_SHORT_URL.format(custom_id))
            if custom_id == '' or custom_id is None:
                data['custom_id'] = get_unique_short_id()
            elif not re.match(SHORT_REGEX, custom_id):
                raise InvalidAPIUsage(VALID_SHORT)
        else:
            data['custom_id'] = get_unique_short_id()
        return URLMap.adding_into_db(data['url'], data['custom_id'])

    @staticmethod
    def short_url_view(form):
        original_url = form.original_link.data
        short_url = form.custom_id.data
        if short_url:
            if URLMap.query.filter_by(short=short_url).first() is not None:
                flash(SHORT_URL_EXISTS.format(short_url))
            else:
                URLMap.adding_into_db(original_url, short_url)
                return render_template('url.html', url=short_url, form=form)
        short_url = get_unique_short_id()
        URLMap.adding_into_db(original_url, short_url)
        return render_template('url.html', url=short_url, form=form)
