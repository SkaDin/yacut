import string
import random

from flask import flash, redirect, render_template, url_for

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URLMap
from yacut.contants import SHORT_URL_LENGTH


def get_unique_short_id(length=SHORT_URL_LENGTH):
    """
    Алгоритм формирования коротких идентификаторов переменной длины.
    """
    seq = string.ascii_letters + string.digits
    existing_urls = URLMap.query.all()
    # Создаём множество всех имеющихся url-адресов.
    existing_ids = {url.short for url in existing_urls}
    # И в бесконечном цикле создаём короткий id и проверяем.
    while True:
        new_short_id = ''.join(random.choices(seq, k=length))
        if new_short_id not in existing_ids:
            # Если такого id в БД нет,
            # прерываем цикл, возвращая сгенерированный id.
            return new_short_id
        else:
            # Если же коллизия произошла - продолжаем цикл.
            continue


@app.route('/', methods=['GET', 'POST'])
def add_url_view():
    """Форма на главной странице."""
    form = URLForm()
    if form.validate_on_submit():
        short = form.custom_id.data or get_unique_short_id()
        url = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        flash(url_for('url_view', short=short, _external=True))
    return render_template('url.html', form=form)


@app.route('/<string:short>')
def url_view(short):
    """Функция перенаправления с короткой ссылки на длинную."""
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original)
