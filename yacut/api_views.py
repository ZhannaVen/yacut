import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .constants import (CHANGE_SHORT_URL, EMPTY, EMPTY_ID, EMPTY_URL,
                        SHORT_REGEX, VALID_SHORT)
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def new_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY)
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
    new_url = URLMap()
    new_url.from_dict(data)
    db.session.add(new_url)
    db.session.commit()
    return jsonify(new_url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage(EMPTY_ID, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK