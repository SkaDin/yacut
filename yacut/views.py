import random
import string

from flask import flash, redirect, render_template, url_for

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URLMap


def get_unique_short_id(length=6):
    """
    Алгоритм формирования коротких идентификаторов переменной длины.
    """
    seq = string.ascii_letters + string.digits
    if not URLMap.query.filter_by(short=seq).first():
        return ''.join(random.choices(seq, k=length))


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
