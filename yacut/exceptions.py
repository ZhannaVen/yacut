class ValidationError(Exception):
    """Ошибка при несоответствии урла регулярному
    выражению или количеству символов.
    """
    pass


class UniqueShortError(Exception):
    """Сервис не смог подобрать имя для короткой ссылки.
    """
    pass


class AlreadyExistsError(Exception):
    """В базе данных уже существует данное значение.
    """
    pass
