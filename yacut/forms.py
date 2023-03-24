from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from .models import SHORT_REGEX

INSERT_LINK = 'Обязательное поле'
MAX_1 = 1024
URL_FIELD = 'Здесь должен быть url-адрес'
ADD_URL = 'Вставьте ссылку'
SHORT_URL = 'Короткая ссылка'
MAX_2 = 16
NUMBER_OF_SYMBOLS = 'Допустимо не более 16 символов'
ALLOWABLE_SYMBOLS = 'Для короткой ссылки допустимы только цифры 0-9 и буквы "a-Z"'
ADD = 'Добавить'


class URLMapForm(FlaskForm):
    original_link = URLField(
        ADD_URL,
        validators=[
            DataRequired(message=INSERT_LINK),
            Length(max=MAX_1),
            URL(require_tld=False, message=URL_FIELD)
        ]
    )
    custom_id = StringField(
        SHORT_URL,
        validators=[
            Length(max=MAX_2, message=NUMBER_OF_SYMBOLS),
            Optional(),
            Regexp(
                regex=SHORT_REGEX,
                message=ALLOWABLE_SYMBOLS)
        ]
    )
    submit = SubmitField(ADD)
