from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField,BooleanField
from wtforms.validators import DataRequired,EqualTo,Length


class sign_up_form_class(FlaskForm):
    username_field = StringField("Username", validators=[DataRequired(),Length(max=32)])
    password_field = PasswordField("Password", validators=[DataRequired()])
    re_enter_password = PasswordField("Re Enter Password",validators=[DataRequired(),EqualTo('password_field')])
    Sign_up = SubmitField("Sign Up")

class sign_in_form_class(FlaskForm):
    username_field = StringField("Username", validators=[DataRequired(),Length(max=32)])
    password_field = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    Sign_in = SubmitField("Sign In")


class new_room_class(FlaskForm):
    Room_ID_Field = StringField("Enter New Room Id", validators=[DataRequired(),Length(max=32)])
    Room_Name_Field = StringField("Enter Room Name", validators=[DataRequired(),Length(max=100)])
    Create_Room = SubmitField("Create Room")

class go_to_room_class(FlaskForm):
    Room_ID_Field = StringField("Enter Your Room Id", validators=[DataRequired(),Length(max=32)])
    go_to_room = SubmitField("Go To Room")

class send_message_class(FlaskForm):
    message = TextAreaField("Type Your Message",validators=[Length(max=1024)])
    Send_message = SubmitField("Send")

