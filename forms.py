from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired,EqualTo


class sign_up_form_class(FlaskForm):
    username_field = StringField("Username", validators=[DataRequired()])
    password_field = PasswordField("Password", validators=[DataRequired()])
    re_enter_password = PasswordField("Re Enter Password",validators=[DataRequired(),EqualTo('password_field')])
    Sign_up = SubmitField("Sign Up")

class sign_in_form_class(FlaskForm):
    username_field = StringField("Username", validators=[DataRequired()])
    password_field = PasswordField("Password", validators=[DataRequired()])
    Sign_in = SubmitField("Sign In")

class new_room_class(FlaskForm):
    Room_ID_Field = StringField("Enter New Room Id", validators=[DataRequired()])
    Room_Name_Field = StringField("Enter Room Name", validators=[DataRequired()])
    Create_Room = SubmitField("Create Room")

class go_to_room_class(FlaskForm):
    Room_ID_Field = StringField("Enter Your Room Id", validators=[DataRequired()])
    go_to_room = SubmitField("Go To Room")

class send_message_class(FlaskForm):
    message = TextAreaField("Type Your Message", validators=[DataRequired()])
    Send_message = SubmitField("Send")

