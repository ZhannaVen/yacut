from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    original = URLField(
        'Вставьте ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    short = URLField(
        'Короткая ссылка',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Добавить')