from flask import Blueprint, render_template, redirect, url_for, flash

# Modelos
from ...models import Books, Authors, Publishers

# Forms
from ...forms import BookForm

# DB
from biblioflask import db


books_bp = Blueprint('books', __name__, url_prefix='/books')


@books_bp.route('/')
def list_books():
    books = Books.query.all()

    ctx = {
        'books': books
    }

    return render_template('books/list.html', **ctx)


@books_bp.route('/add-book/', methods=['GET', 'POST'])
def add_book():
    form = BookForm()

    # Obtener la lista de autores y publishers para cargar en los campos select
    authors = Authors.query.all()
    publishers = Publishers.query.all()
    form.authors.choices = [(author.id, f'{author.name} {author.lastname}') for author in authors]
    form.publisher_id.choices = [(publisher.id, publisher.name) for publisher in publishers]

    if form.validate_on_submit():
        # Crear una instancia de Book con los datos del formulario
        book = Books(
            title=form.title.data,
            pub_date=form.pub_date.data,
            publisher_id=form.publisher_id.data
        )

        # Obtener los autores seleccionados del formulario y agregarlos al libro
        selected_author_ids = form.authors.data
        selected_authors = Authors.query.filter(Authors.id.in_(selected_author_ids)).all()
        book.authors.extend(selected_authors)

        # Guardar el libro en la base de datos
        db.session.add(book)
        db.session.commit()

        flash('El libro ha sido añadido correctamente.', 'success')

        # Redireccionar a la página de lista de libros
        return redirect(url_for('books.list_books'))

    ctx = {
        'title': "Añadir Libro",
        'form': form
    }

    return render_template('books/form.html', **ctx)


@books_bp.route('/delete-book/<int:book_id>')
def delete_book(book_id):

    # Obtenemos la instancia del libro
    book = Books.query.get_or_404(book_id)

    # Eliminar el libro de la base de datos
    db.session.delete(book)
    db.session.commit()

    flash('El libro ha sido eliminado correctamente.', 'success')

    # Redireccionar a la página de lista de libros
    return redirect(url_for('books.list_books'))


@books_bp.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Books.query.get_or_404(book_id)
    form = BookForm(obj=book)

    # Obtener la lista de autores y publishers para cargar en los campos select
    authors = Authors.query.all()
    publishers = Publishers.query.all()
    form.authors.choices = [(author.id, author.name) for author in authors]
    form.publisher_id.choices = [(publisher.id, publisher.name) for publisher in publishers]

    if form.validate_on_submit():
        # Actualizar los datos del libro con los datos del formulario
        book.title = form.title.data
        book.pub_date = form.pub_date.data
        book.publisher_id = form.publisher_id.data

        # Obtener los autores seleccionados del formulario y asignarlos al libro
        selected_author_ids = form.authors.data
        selected_authors = Authors.query.filter(Authors.id.in_(selected_author_ids)).all()
        book.authors = selected_authors

        # Guardar los cambios en la base de datos
        db.session.commit()

        flash('El libro ha sido editado correctamente.', 'success')
        # Redireccionar a la página de lista de libros
        return redirect(url_for('books.list_books'))

    # Establecer los valores seleccionados en el campo authors
    form.authors.data = [author.id for author in book.authors]

    ctx = {
        'title': "Editar Libro",
        'book': book,
        'form': form,
        'edit_mode': True
    }

    return render_template('books/form.html', **ctx)
