from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class OpinionForm(FlaskForm):
    original = URLField(
        'Вставьте ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    short = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Добавить')