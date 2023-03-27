from flask import flash, redirect, render_template, url_for

from . import app
from .exceptions import AlreadyExistsError
from .forms import URLMapForm
from .models import URLMap

SHORT_URL_EXISTS = 'Имя {} уже занято!'
ERROR = 'Сервис не смог подобрать подходящее имя. Попробуйте снова.'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original_url = form.original_link.data
    short_url = form.custom_id.data
    try:
        new_url = URLMap.get_new_record(original_url, short_url)
    except AlreadyExistsError:
        flash(SHORT_URL_EXISTS.format(short_url))
        return render_template('index.html', form=form)
    except ValueError:
        flash(ERROR)
        return render_template('index.html', form=form)
    return render_template(
        'index.html',
        url=url_for('redirect_view', short=new_url.short, _external=True),
        form=form
    )


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(URLMap.get_or_404(short))
