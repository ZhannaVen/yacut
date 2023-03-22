import shortuuid

from . import db
from .models import URLMap


def get_unique_short_id():
    short_url = shortuuid.ShortUUID().random(length=16)
    if URLMap.query.filter_by(short=short_url).first() is not None:
        return get_unique_short_id()
    return short_url


def adding_into_db(original_url, short_url):
    db.session.add(URLMap(
        original=original_url,
        short=short_url,
    ))
    db.session.commit()