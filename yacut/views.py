from flask import flash, redirect, render_template, url_for

from . import app
from .exceptions import AlreadyExistsError, GetShortError
from .forms import URLMapForm
from .models import URLMap

SHORT_URL_EXISTS = 'Имя {} уже занято!'
FAILED_ATTEMPT = 'Сервис не смог подобрать имя.'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original_url = form.original_link.data
    short_url = form.custom_id.data
    try:
        new_record = URLMap.get_new_record(original_url, short_url)
        return render_template(
            'index.html',
            url=url_for('redirect_view', short=new_record.short, _external=True),
            form=form
        )
    except AlreadyExistsError:
        flash(SHORT_URL_EXISTS.format(short_url))
    except GetShortError:
        flash(FAILED_ATTEMPT)
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(URLMap.get_or_404(short))
