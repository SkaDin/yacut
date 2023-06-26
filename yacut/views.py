import uuid

from flask import flash, redirect, render_template, url_for

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URLMap
from yacut.contants import SHORT_URL_LENGTH


def get_unique_short_id():
    """
    Алгоритм формирования коротких идентификаторов переменной длины.
    """
    # seq = string.ascii_letters + string.digits
    # Мы создаём множество всех имеющихся url-адресов.
    # existing_ids = {url.short for url in existing_urls}
    # while True:
    #    new_short_id = ''.join(random.choices(seq, k=length))
    #    if new_short_id not in existing_ids:
    #         Если такого id в БД нет,
    #         прерываем цикл, возвращая сгенерированный id.
    #        return new_short_id

    # Я решил использовать бибилотеку uuid по 3 причинам:
    # 1 - библиотека обеспечивает уникальность каждого короткого id;
    # 2 - меньшая потенциальная нагрузка на сервер;
    # 3 - читабельность кода;
    return str(uuid.uuid4().hex)[:SHORT_URL_LENGTH]


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
