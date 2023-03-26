class ShortUrlError(Exception):
    """Ошибка при несоответствии урла регулярному выражению
    или количеству символов.
    """
    pass


class RepeatError(Exception):
    """В базе данных уже существует данное значение.
    """
    pass