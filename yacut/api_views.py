from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .exceptions import AlreadyExistsError, ShortUrlError, LongUrlError
from .models import URLMap
from settings import MAX_LONG


LONG_TOO_LONG = f'Максимальная длина урла: {MAX_LONG} символов.'
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
        new_record = URLMap.get_new_record(original_url, short_url)
    except AlreadyExistsError:
        raise InvalidAPIUsage(CHANGE_SHORT_URL.format(short_url))
    except ShortUrlError:
        raise InvalidAPIUsage(VALID_SHORT)
    except ValueError:
        raise InvalidAPIUsage(ERROR)
    except LongUrlError:
        raise InvalidAPIUsage(LONG_TOO_LONG)
    return jsonify(new_record.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    try:
        url = URLMap().get_original_url(short_id)
    except ValueError:
        raise InvalidAPIUsage(EMPTY_ID, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url}), HTTPStatus.OK
