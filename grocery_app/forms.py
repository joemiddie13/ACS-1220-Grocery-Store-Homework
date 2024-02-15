from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, URL
from wtforms_sqlalchemy.fields import QuerySelectField
from grocery_app.models import GroceryStore

def store_query():
    return GroceryStore.query

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""

    # TODO: Add the following fields to the form class:
    # - title - StringField
    # - address - StringField
    # - submit button
    title = StringField('Title', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""

    # TODO: Add the following fields to the form class:
    # - name - StringField
    # - price - FloatField
    # - category - SelectField (specify the 'choices' param)
    # - photo_url - StringField
    # - store - QuerySelectField (specify the `query_factory` param)
    # - submit button
    name = StringField('Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    category = SelectField('Category', choices=[('PRODUCE', 'Produce'), ('DELI', 'Deli'), ('BAKERY', 'Bakery'), ('PANTRY', 'Pantry'), ('FROZEN', 'Frozen'), ('OTHER', 'Other')], validators=[DataRequired()])
    photo_url = StringField('Photo URL', validators=[Optional(), URL()])
    store = QuerySelectField('Store', query_factory=store_query, allow_blank=False, get_label='title')
    submit = SubmitField('Submit')