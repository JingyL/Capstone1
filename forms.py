from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, SelectField,TextAreaField

from wtforms.validators import InputRequired, Optional, URL


class boardForm(FlaskForm):
    """Form for adding playlists."""

    # Add the necessary code to use this form
    name = StringField("name", validators=[
                       InputRequired(message="Name can't be blank")])
 

class listForm(FlaskForm):
    """Form for adding playlists."""

    # Add the necessary code to use this form
    name = StringField("name", validators=[
                       InputRequired(message="Name can't be blank")])