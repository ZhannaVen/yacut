from . import app, db
from .forms import URLMapForm
from flask import flash, redirect, render_template, abort
from .models import URLMap
from http import HTTPStatus
import shortuuid


SHORT_URL_EXISTS = 'Короткая ссылка занята. Придумайте другую или воспользуйтесь предложенной.'


def get_unique_short_id():
    short_url = shortuuid.ShortUUID().random(length=16)
    return short_url


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original_url = form.original.data
        short_url = form.short.data
        if short_url:
            if URLMap.query.filter_by(short=short_url).first() is not None:
                new_short_url = get_unique_short_id()
                flash(SHORT_URL_EXISTS)
                new_url = URLMap(
                    original=form.original.data,
                    short=new_short_url,
                )
                db.session.add(new_url)
                db.session.commit()
                return render_template('url.html', url=new_short_url, form=form)
            new_url = URLMap(
                original=original_url,
                short=short_url,
            )
            db.session.add(new_url)
            db.session.commit()
            return render_template('url.html', url=short_url, form=form)
        short_url = get_unique_short_id()
        new_url = URLMap(
            original=original_url,
            short=short_url,
        )
        db.session.add(new_url)
        db.session.commit()
        return render_template('url.html', url=short_url, form=form)
    return render_template('url.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    url = URLMap.query.filter_by(short=short).first()
    if url is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url.original, 301)

