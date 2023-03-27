class ShortUrlError(Exception):
    """Ошибка при несоответствии урла регулярному выражению
    или количеству символов.
    """
    pass


class LongUrlError(Exception):
    """Ошибка при несоответствии урла количеству символов.
    """
    pass


class AlreadyExistsError(Exception):
    """В базе данных уже существует данное значение.
    """
    pass
