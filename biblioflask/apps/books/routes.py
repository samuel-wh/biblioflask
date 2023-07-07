from flask import Blueprint, render_template, redirect, url_for

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
    return render_template('books/list_books.html', books=books)


@books_bp.route('/add-book/', methods=['GET', 'POST'])
def add_book():
    form = BookForm()

    # Obtener la lista de autores y publishers para cargar en los campos select
    authors = Authors.query.all()
    publishers = Publishers.query.all()
    form.authors.choices = [(author.id, author.name) for author in authors]
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

        # Redireccionar a la página de lista de libros
        return redirect(url_for('books.list_books'))

    return render_template('books/add_book.html', form=form)
