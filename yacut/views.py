import random
import string

from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URLMap


def generate_seq(length=6):
    """Функция генерации случайной короткой части длинной 6 символов."""
    seq = string.ascii_letters + string.digits
    if not URLMap.query.filter_by(short=seq).first():
        return ''.join(random.choices(seq, k=length))


@app.route('/', methods=['GET', 'POST'])
def add_url_view():
    """Функция записи ссылок в БД"""
    form = URLForm()
    if form.validate_on_submit():
        short = form.custom_id.data or generate_seq()
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
    """Функция 'склеивания' адреса сайта с составной частью(short)."""
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original)
