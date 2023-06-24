from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp, ValidationError

from yacut.models import URLMap


class URLForm(FlaskForm):
    original_link = URLField(
        'Ваша длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), URL(
            require_tld=True, message='Некорректный URL')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 16), Optional(), Regexp(
            r'^[A-Za-z0-9]+$',
            message='Можно использовать только [A-Za-z0-9] '
                    'длинной не более 6 символов')]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if field.data and URLMap.query.filter_by(short=field.data).first():
            raise ValidationError(f'Название {field.data} уже занято!')
