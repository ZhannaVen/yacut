from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


SHORT_REGEX = r'^[a-zA-Z\d]{1,16}$'


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Вставьте ссылку',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 128),
            URL(require_tld=False, message='Здесь должен быть url-адрес')
        ]
    )
    custom_id = StringField(
        'Короткая ссылка',
        validators=[
            Length(1, 16, message='Допустимо не более 16 символов'),
            Optional(),
            Regexp(
                regex=SHORT_REGEX,
                message='Допустимы только цифры 0-9 и буквы "a-Z"')
        ]
    )
    submit = SubmitField('Добавить')