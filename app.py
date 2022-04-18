from flask import Flask, render_template, request, redirect, url_for,flash
from forms import sign_up_form_class, sign_in_form_class, new_room_class, send_message_class,go_to_room_class
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'whatever123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)




class user(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    password_hash = db.Column(db.String(128), index=False)
    joined_at = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    messages = db.relationship('messages', backref='user', lazy='dynamic')


class room(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    room_name = db.Column(db.String(100), index=False)
    created_at = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    messages = db.relationship('messages', backref='room', lazy='dynamic')

    def __init__(self,id,room_name):
        self.id=id
        self.room_name=room_name


class messages(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    room_id = db.Column(db.String(32), db.ForeignKey('room.id'), index=True)
    username = db.Column(db.String(32), db.ForeignKey('user.id'), index=True)
    message_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)



@app.route('/', methods=["GET", "POST"])
def main():  # put application's code here
    return render_template('home.html')


@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    sign_up_form_obj = sign_up_form_class(csrf_enabled=False)
    if sign_up_form_obj.validate_on_submit() and user.query.get(sign_up_form_obj.username_field.data) == None:
        new_user = user(id=sign_up_form_obj.username_field.data,
                        password_hash=generate_password_hash(sign_up_form_obj.password_field.data))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('sign_in'))
    return render_template('sign_up.html', sign_up_form=sign_up_form_obj)



@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    sign_in_form_obj = sign_in_form_class(csrf_enabled = False)
    if sign_in_form_obj.validate_on_submit():
        pass
    else:
        pass
    return render_template("sign_in.html", sign_in_form=sign_in_form_obj)


@app.route('/create_room', methods = ["GET", "POST"])
def create_room():
    create_room_form_obj = new_room_class()
    if create_room_form_obj.validate_on_submit() :
        new_room = room(id = create_room_form_obj.Room_ID_Field.data,room_name=create_room_form_obj.Room_Name_Field.data)
        db.session.add(new_room)
        db.session.commit()
        return redirect(url_for('go_to_room'))
    return render_template('create_room.html', create_room_form=create_room_form_obj)



@app.route('/go_to_room', methods = ["GET", "POST"])
def go_to_room():
    go_to_room_form_obj = go_to_room_class()
    if go_to_room_form_obj.validate_on_submit():
        pass
    return render_template('Go_to_room.html', go_to_room_form = go_to_room_form_obj)



@app.route('/room/<string:id>', methods = ["GET", "POST"])
def room(id):
    send_message_form_obj = send_message_class()
    if send_message_form_obj.validate_on_submit():
        pass
    else:
        pass
    return render_template('chat_room.html', send_message_form = send_message_form_obj)



if __name__ == '__main__':
    app.run()
