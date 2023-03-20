import shortuuid


def get_unique_short_id():
    return shortuuid.ShortUUID().random(length=16)


def get_full_url_view():
    pass