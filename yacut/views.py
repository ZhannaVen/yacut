from . import app
from .forms import URLMapForm
from flask import abort, flash, redirect, render_template, url_for
from .messages import URL_EXISTS, SHORT_URL_EXISTS
from .models import URLMap
from .utils import get_unique_short_id

@app.route('/')
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original_url = form.original.data
        object_original = URLMapForm.query.filter_by(original=original_url).first()
        if object_original:
            short_url = getattr(object_original, 'short')
            flash(URL_EXISTS.format(short_url))
            return render_template('url.html', form=form)
        short_url = form.short.data
        if short_url:
            object_short = URLMapForm.query.filter_by(short=short_url).first()
            if object_short:
                short_url = get_unique_short_id()
                flash(SHORT_URL_EXISTS.format(short_url))
                return render_template('url.html', form=form)
        

        

    original_url = 
    return 'Это мой второй Flask-проект'


@app.route('/<string:short>')
def get_full_url_view():
    pass
