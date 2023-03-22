from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .constants import SHORT_URL_EXISTS
from .forms import URLMapForm
from .models import URLMap
from .utils import adding_into_db, get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original_url = form.original_link.data
        short_url = form.custom_id.data
        if short_url:
            if URLMap.query.filter_by(short=short_url).first() is not None:
                short_url = get_unique_short_id()
                flash(SHORT_URL_EXISTS)
            else:
                adding_into_db(original_url, short_url)
                return render_template('url.html', url=short_url, form=form)
        short_url = get_unique_short_id()
        adding_into_db(original_url, short_url)
        return render_template('url.html', url=short_url, form=form)
    return render_template('url.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    url = URLMap.query.filter_by(short=short).first()
    if url is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url.original, 301)
