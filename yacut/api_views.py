from http import HTTPStatus
from re import match

from flask import jsonify, request
from validators import url

from . import app, db
from .constants import (CHANGE_SHORT_URL, EMPTY, EMPTY_ID, EMPTY_URL,
                        INVALID_URL, SHORT_REGEX, VALID_SHORT)
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/<string:short_id>', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage(EMPTY_ID, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY)
    if 'url' not in data:
        raise InvalidAPIUsage(EMPTY_URL)
    original = data.get('url')
    if not url(original):
        raise InvalidAPIUsage(INVALID_URL.format(original))
    short = data.get('short_link')
    if short:
        if not match(SHORT_REGEX, short):
            raise InvalidAPIUsage(VALID_SHORT.format(short))
        if URLMap.query.filter_by(short=short).first() is not None:
            raise InvalidAPIUsage(CHANGE_SHORT_URL.format(short))
    else:
        short = get_unique_short_id()
    new_url = URLMap()
    new_url.from_dict(data)
    db.session.add(new_url)
    db.session.commit()
    return jsonify(new_url.to_dict()), HTTPStatus.CREATED