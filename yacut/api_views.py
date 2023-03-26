from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .exceptions import RepeatError, ShortUrlError
from .models import URLMap

EMPTY = 'Отсутствует тело запроса'
EMPTY_URL = '"url" является обязательным полем!'
CHANGE_SHORT_URL = 'Имя "{}" уже занято.'
VALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
EMPTY_ID = 'Указанный id не найден'
ERROR = 'Сервис не смог подобрать подходящее имя. Попробуйте снова.'


@app.route('/api/id/', methods=['POST'])
def new_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY)
    if 'url' not in data:
        raise InvalidAPIUsage(EMPTY_URL)
    original_url = data.get('url')
    short_url = data.get('custom_id')
    try:
        new_url = URLMap().short_url(original_url, short_url)
    except RepeatError:
        raise InvalidAPIUsage(CHANGE_SHORT_URL.format(short_url))
    except ShortUrlError:
        raise InvalidAPIUsage(VALID_SHORT)
    except ValueError:
        raise InvalidAPIUsage(ERROR)
    return jsonify(new_url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    try:
        url = URLMap().get_original_url(short_id)
    except ValueError:
        raise InvalidAPIUsage(EMPTY_ID, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url}), HTTPStatus.OK
