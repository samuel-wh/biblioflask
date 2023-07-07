from flask import Blueprint, render_template, redirect, url_for

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
    return render_template('publishers/add.html', form=form)