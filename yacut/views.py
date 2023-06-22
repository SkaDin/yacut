from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URLMap


@app.route('/')
def index_view():
    return render_template('url.html')
