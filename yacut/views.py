from . import app, db
from .forms import URLMapForm
from flask import flash, redirect, render_template
from .messages import URL_EXISTS, SHORT_URL_EXISTS
from .models import URLMap
from .utils import get_unique_short_id
from settings import SITE
import shortuuid


def get_unique_short_id():
    return shortuuid.ShortUUID().random(length=16)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original_url = form.original.data
        url = URLMap.query.filter_by(original=original_url).first()
        if url:
            flash(URL_EXISTS.format(SITE, url.short))
            return render_template('url.html', form=form, url=url)
        short_url = form.short.data
        if short_url:
            url = URLMap.query.filter_by(short=short_url).first()
            if url:
                new_short_url = get_unique_short_id()
                flash(SHORT_URL_EXISTS.format(SITE, new_short_url))
                url = URLMap(
                    original=form.original.data,
                    short=new_short_url,
                )
                db.session.add(url)
                db.session.commit()
                return render_template('url.html', url=url)
        short_url = get_unique_short_id()
        url = URLMap(
            original=form.original.data,
            short=short_url,
        )
        db.session.add(url)
        db.session.commit()
        return render_template('url.html', url=url)
    return render_template('url.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    url = URLMap.query.filter_by(short=short).first()
    return redirect(url.original, 301)
