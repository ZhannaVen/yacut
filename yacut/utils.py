import shortuuid
from .models import URLMap


def get_unique_short_id():
    short_url = shortuuid.ShortUUID().random(length=16)
    if URLMap.query.filter(short=short_url).first is None:
        return short_url
    return get_unique_short_id()
