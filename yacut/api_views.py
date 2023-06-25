from http import HTTPStatus
from re import match

from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.views import get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original(short_id):
    """
    Функция получения оригинальной ссылки
     по указанному короткому идентификатору.
     """
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_id():
    """Функция POST-запроса на создание новой короткой ссылки."""
    data = request.get_json()
    validate_create_id(data)
    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED


def validate_create_id(data):
    """Фунция валидации данных из запроса."""
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not match(
            r'^[a-z]+://[^\/\?:]+(:[0-9]+)?(\/.*?)?(\?.*)?$', data['url']):
        raise InvalidAPIUsage('Указан недопустимый URL')
    if not data.get('custom_id'):
        data['custom_id'] = get_unique_short_id()
        return HTTPStatus.CREATED
    if not match(r'^[A-Za-z0-9]{1,16}$', data['custom_id']):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки'
        )
    if URLMap.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
