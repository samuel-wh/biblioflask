from flask import Blueprint, render_template, redirect, url_for, flash

# Modelos
from ...models import Books, Authors, Publishers

# Forms
from ...forms import PublisherForm

# DB
from biblioflask import db


publishers_bp = Blueprint('publishers', __name__, url_prefix='/publishers')


@publishers_bp.route('/')
def list_publishers():
    publishers = Publishers.query.all()
    ctx = {
        'publishers': publishers
    }
    return render_template('publishers/list.html', **ctx)


@publishers_bp.route('/add-publisher/', methods=['GET', 'POST'])
def add_publisher():
    form = PublisherForm()
    if form.validate_on_submit():

        # Creamos la instancia de la base de datos
        publisher = Publishers(
            name=form.name.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            country=form.country.data,
            website=form.website.data
        )
        db.session.add(publisher)
        db.session.commit()
        return redirect(url_for('publishers.list_publishers'))
    ctx = {
        'title': "Agregar Editorial",
        'form': form,
    }
    return render_template('publishers/form.html', **ctx)


@publishers_bp.route('/delete-publisher/<int:publisher_id>')
def delete_publisher(publisher_id):
    # Obtenemos la instancia de la editorial
    publisher = Publishers.query.get_or_404(publisher_id)

    # Eliminar la editorial de la base de datos
    db.session.delete(publisher)
    db.session.commit()

    flash('La editorial ha sido eliminado correctamente', 'success')

    return redirect(url_for('publishers.list_publishers'))


@publishers_bp.route('/edit-publisher/<int:publisher_id>/', methods=['GET', 'POST'])
def edit_publisher(publisher_id):
    # Obtenemos la instancia de la editorial
    publisher = Publishers.query.get_or_404(publisher_id)

    form=PublisherForm(obj=publisher)


    if form.validate_on_submit():
        # Actualizamos los datos de la instancia
        publisher.name = form.name.data
        publisher.address = form.address.data
        publisher.city = form.city.data
        publisher.state = form.state.data
        publisher.country = form.country.data
        publisher.website = form.website.data
        db.session.commit()
        flash('La editorial ah sido editado correctamente', 'success')
        return redirect(url_for('publishers.list_publishers'))

    ctx = {
        'title': "Editar Editorial",
        'publisher': publisher,
        'form': form,
        'edit_mode': True
    }
    return render_template('publishers/form.html', **ctx)