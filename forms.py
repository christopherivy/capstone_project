from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    SelectField,
    IntegerField,
    validators,
)
from wtforms.validators import DataRequired, Email, Length


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[Length(min=6)])
    image_url = StringField("(Optional) Image URL")


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])


class SearchForm(FlaskForm):
    """Search form."""

    # genres = SelectField("Genres", choices=["action", "comedy"])
    title = StringField("Enter a Movie Title", validators=[DataRequired()])
    # year = IntegerField("Enter a Movie Year", validators=[validators.optional()])
