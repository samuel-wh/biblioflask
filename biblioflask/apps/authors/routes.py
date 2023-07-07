from flask import Blueprint, render_template, redirect, url_for

# Modelos
from ...models import Authors

# Forms
from ...forms import AuthorForm

# DB
from biblioflask import db


authors_bp = Blueprint('authors', __name__, url_prefix='/authors')

@authors_bp.route('/')
def list_authors():
    authors = Authors.query.all()
    return render_template('authors/list.html', authors=authors)


@authors_bp.route('/add-author/', methods=['GET', 'POST'])
def add_author():
    form = AuthorForm()
    if form.validate_on_submit():
        author = Authors(
            name=form.name.data,
            lastname=form.lastname.data,
            email=form.email.data
        )
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('authors.list_authors'))
    return render_template('authors/add.html', form=form)