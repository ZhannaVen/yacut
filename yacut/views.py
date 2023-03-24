from flask import redirect, render_template

from . import app
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('url.html', form=form)
    return URLMap().short_url_view(form)


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(URLMap.get_or_404(short))
