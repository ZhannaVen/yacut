class ShortNameError(Exception):
    """Ошибка при несоответствии урла регулярному выражению.
    """
    pass


class ShortLengthError(Exception):
    """Ошибка при несоответствии имени количеству символов.
    """
    pass


class LongUrlError(Exception):
    """Ошибка при несоответствии урла количеству символов.
    """
    pass


class GetShortError(Exception):
    """Сервис не смог подобрать имя для короткой ссылки.
    """
    pass


class AlreadyExistsError(Exception):
    """В базе данных уже существует данное значение.
    """
    pass
