from flask_wtf import FlaskForm
from settings import MAX_LONG, MAX_SHORT, SHORT_REGEX
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

INSERT_LINK = 'Обязательное поле'
URL_FIELD = 'Здесь должен быть url-адрес'
ADD_URL = 'Вставьте ссылку'
SHORT_URL = 'Короткая ссылка'
NUMBER_OF_SYMBOLS = f'Допустимо не более {MAX_SHORT} символов'
SYMBOLS = 'Допустимы только цифры 0-9 и буквы "a-Z"'
ADD = 'Добавить'


class URLMapForm(FlaskForm):
    original_link = URLField(
        ADD_URL,
        validators=[
            DataRequired(message=INSERT_LINK),
            Length(max=MAX_LONG),
            URL(require_tld=False, message=URL_FIELD)
        ]
    )
    custom_id = StringField(
        SHORT_URL,
        validators=[
            Length(1, 16),
            Optional(),
            Regexp(
                regex=SHORT_REGEX,
                message=SYMBOLS)
        ]
    )
    submit = SubmitField(ADD)
