from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import DataRequired, Length, Optional, URL, UUID


class URLMapForm(FlaskForm):
    original = URLField(
        'Вставьте ссылку',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 128),
            URL(require_tld=False, message='Здесь должен быть url-адрес')
        ]
    )
    short = StringField(
        'Короткая ссылка',
        validators=[
            Length(1, 16, message='Допустимо не более 16 символов'),
            Optional(),
            UUID(message='Допустимы следующие символы: A_Z, a-z, 0-9')
        ]
    )
    submit = SubmitField('Добавить')