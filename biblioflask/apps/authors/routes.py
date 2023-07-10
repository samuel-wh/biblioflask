from flask import Blueprint, render_template, redirect, url_for, flash

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

    ctx = {
        'authors': authors
    }

    return render_template('authors/list.html', **ctx)


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
        flash('El autor ha sido añadido correctamente.', 'success')
        return redirect(url_for('authors.list_authors'))
    
    ctx = {
        'title': "Añadir autor",
        'form': form
    }

    return render_template('authors/form.html', **ctx)


@authors_bp.route('delete-author/<int:author_id>')
def delete_author(author_id):

    # Obtenemos la instacia del author
    auhor = Authors.query.get_or_404(author_id)

    # Eliminar el autor de la base de datos
    db.session.delete(auhor)
    db.session.commit()

    flash('El autor ha sido eliminado correctamente.', 'success')

    return redirect(url_for('authors.list_authors'))


@authors_bp.route('/edit-author/<int:author_id>', methods=['GET', 'POST'])
def edit_author(author_id):
    author = Authors.query.get_or_404(author_id)
    form = AuthorForm(obj=author)

    if form.validate_on_submit():
        author.name = form.name.data,
        author.lastname = form.lastname.data,
        author.email = form.email.data

        db.session.commit()
        flash('El autor ha sido editado correctamente.', 'success')
        return redirect(url_for('authors.list_authors'))
    
    ctx = {
        'title': "Editar autor",
        'author': author,
        'form': form,
        'edit_mode': True
    }

    return render_template('authors/form.html', **ctx)