

from flask import flash, redirect, render_template

from . import app
from .forms import URLMapForm
from .models import URLMap

SHORT_URL_EXISTS = 'Имя {} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original_url = form.original_link.data
    short_url = form.custom_id.data
    try:
        new_url = URLMap().short_url_api(original_url, short_url)
    except NameError:
        flash(SHORT_URL_EXISTS.format(short_url))
        return render_template('index.html', form=form)
    return render_template('index.html', url=new_url.short, form=form)


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(URLMap.get_or_404(short))
