from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import OpinionForm
from .models import Opinion


@app.route('/', methods=['POST'])
def index_view():
    pass
    

@app.route('/<string:id>', methods=['GET'])
def get_full_url_view():
    pass
