from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

EMPTY = 'Отсутствует тело запроса'
EMPTY_URL = '"url" является обязательным полем!'


@app.route('/api/id/', methods=['POST'])
def new_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY)
    new_url = URLMap()
    new_url = new_url.short_url_api(data)
    return jsonify(new_url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap()
    url = url.get_original_url(short_id)
    return jsonify({'url': url}), HTTPStatus.OK
