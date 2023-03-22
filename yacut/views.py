from http import HTTPStatus

import shortuuid
from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap


SHORT_URL_EXISTS = 'Короткая ссылка занята. Придумайте другую или воспользуйтесь предложенной.'


def get_unique_short_id():
    short_url = shortuuid.ShortUUID().random(length=16)
    if URLMap.query.filter_by(short=short_url).first() is not None:
        return get_unique_short_id()
    return short_url


def adding_into_db(original_url, short_url):
    db.session.add(URLMap(
        original=original_url,
        short=short_url,
    ))
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original_url = form.original_link.data
        short_url = form.custom_id.data
        if short_url:
            if URLMap.query.filter_by(short=short_url).first() is not None:
                new_short_url = get_unique_short_id()
                flash(SHORT_URL_EXISTS)
                adding_into_db(original_url, new_short_url)
                return render_template('url.html', url=new_short_url, form=form)
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
