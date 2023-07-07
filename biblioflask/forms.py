from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email


class PublisherForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address')
    city = StringField('City')
    state = StringField('State')
    country = StringField('Country')
    website = StringField('Website')
    submit = SubmitField('Submit')


class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    authors = SelectMultipleField('Authors', coerce=int)
    publisher_id = SelectField('Publisher', coerce=int)
    pub_date = DateField('Publication Date', format='%Y-%m-%d')
    submit = SubmitField('Submit')


class AuthorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')