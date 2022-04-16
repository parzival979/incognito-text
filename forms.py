from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, equal_to


class sign_up_form_class(FlaskForm):
    username_field = StringField("Username", validators=[DataRequired()])
    password_field = PasswordField("Password", validators=[DataRequired()])
    re_enter_password = PasswordField("Re Enter Password",validators=[DataRequired(), equal_to(password_field)])
    Sign_up = SubmitField("Sign Up")

class sign_in_form_class(FlaskForm):
    username_field = StringField("Username")
    password_field = PasswordField("Password")
    Sign_in = SubmitField("Sign In")

