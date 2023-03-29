from http import HTTPStatus

from flask import jsonify, request
from settings import MAX_LONG

from . import app
from .error_handlers import InvalidAPIUsage
from .exceptions import (AlreadyExistsError, ValidationError, UniqueShortError)
from .models import URLMap

SYMBOLS_NUMBER_LONG = f'Максимальная длина урла: {MAX_LONG} символов.'
EMPTY = 'Отсутствует тело запроса'
EMPTY_URL = '"url" является обязательным полем!'
NAMEL_TAKEN = 'Имя "{}" уже занято.'
INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
ID_NOT_FOUND = 'Указанный id не найден'
FAILED_ATTEMPT = 'Сервис не смог подобрать имя.'


@app.route('/api/id/', methods=['POST'])
def new_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY)
    if 'url' not in data:
        raise InvalidAPIUsage(EMPTY_URL)
    original_url = data.get('url')
    short = data.get('custom_id')
    try:
        return jsonify(URLMap.get_new_record(
            original_url,
            short,
            check_variables=True
        ).to_dict()), HTTPStatus.CREATED
    except AlreadyExistsError:
        raise InvalidAPIUsage(NAMEL_TAKEN.format(short))
    except ValidationError:
        raise InvalidAPIUsage(INVALID_SHORT)
    except UniqueShortError:
        raise InvalidAPIUsage(FAILED_ATTEMPT)
    except Exception as error:
        InvalidAPIUsage(error)


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    try:
        url = URLMap().get_original_url(short_id)
    except ValueError:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url}), HTTPStatus.OK
