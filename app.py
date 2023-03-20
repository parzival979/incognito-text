from datetime import datetime,timedelta
from flask import Flask, render_template, redirect, url_for,request,flash
from flask_login import UserMixin, LoginManager, login_required, login_user,logout_user,current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from forms import sign_up_form_class, sign_in_form_class, new_room_class, send_message_class, go_to_room_class
from os import environ


app = Flask(__name__)
app.config['SECRET_KEY'] = 'whatever123'
uri = environ.get('DATABASE_URL')
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri or 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return user.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
  return render_template('error.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


class user(db.Model, UserMixin):
    id = db.Column(db.String(32), primary_key=True)
    password_hash = db.Column(db.String(128), index=False)
    joined_at = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    messages = db.relationship('messages', backref='user', lazy='dynamic')


class room(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    room_name = db.Column(db.String(100), index=False)
    created_at = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    messages = db.relationship('messages', backref='room', lazy='dynamic')


class messages(db.Model):
    id = db.Column(db.INTEGER,primary_key=True)
    message = db.Column(db.String(1024))
    room_id = db.Column(db.String(32), db.ForeignKey('room.id'), index=True)
    username = db.Column(db.String(32), db.ForeignKey('user.id'), index=True)
    message_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow())


@app.route('/', methods=["GET", "POST"])
def main():  # put application's code here
    return render_template('home.html')


@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    sign_up_form_obj = sign_up_form_class(csrf_enabled=False)
    if sign_up_form_obj.validate_on_submit():
        if user.query.get(sign_up_form_obj.username_field.data) == None:
            new_user = user(id=sign_up_form_obj.username_field.data,password_hash=generate_password_hash(sign_up_form_obj.password_field.data))
            db.session.add(new_user)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                return redirect(url_for('sign_up'))
            return redirect(url_for('sign_in'))
        else:
            flash('Invalid Choice Of Credentials')
    return render_template('sign_up.html', sign_up_form=sign_up_form_obj)


@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    sign_in_form_obj = sign_in_form_class(csrf_enabled=False)
    if sign_in_form_obj.validate_on_submit():
        req_user = user.query.get(sign_in_form_obj.username_field.data)
        if req_user and check_password_hash(req_user.password_hash, sign_in_form_obj.password_field.data):
            login_user(req_user,remember=sign_in_form_obj.remember.data)
            return redirect(url_for('go_to_room'))
        else:
            flash('Invalid Credentials')
            return login_manager.unauthorized()
    return render_template("sign_in.html", sign_in_form=sign_in_form_obj)


@app.route('/create_room', methods=["GET", "POST"])
@login_required
def create_room():
    create_room_form_obj = new_room_class()
    if create_room_form_obj.validate_on_submit() :
        if room.query.get(create_room_form_obj.Room_ID_Field.data) == None:
            new_room = room(id=create_room_form_obj.Room_ID_Field.data, room_name=create_room_form_obj.Room_Name_Field.data)
            db.session.add(new_room)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                return redirect(url_for('create_room'))
            return redirect(url_for('go_to_room'))
        else:
            flash('Chat Room Already Exists')
    return render_template('create_room.html', create_room_form=create_room_form_obj)


@app.route('/go_to_room/', methods=["GET", "POST"])
@login_required
def go_to_room():
    go_to_room_form_obj = go_to_room_class()
    if go_to_room_form_obj.validate_on_submit():
        if not room.query.get(go_to_room_form_obj.Room_ID_Field.data) == None:
            return redirect(url_for('send_message_in_room', id=go_to_room_form_obj.Room_ID_Field.data))
        else:
            flash('Chat Room Does Not Exist')
    return render_template('Go_to_room.html', go_to_room_form=go_to_room_form_obj)


@app.route('/room/<string:id>', methods=["GET", "POST"])
@login_required
def send_message_in_room(id):
    send_message_form_obj = send_message_class()
    if send_message_form_obj.validate_on_submit() and not room.query.get(id) == None and len(send_message_form_obj.message.data)!=0:
        current_message = messages(message = send_message_form_obj.message.data,room_id = id,username=current_user.id,message_time = datetime.utcnow() + timedelta(hours=5,minutes=30))
        db.session.add(current_message)
        db.session.commit()
        return redirect(url_for('send_message_in_room',id = id))
    return render_template('chat_room.html', send_message_form=send_message_form_obj,req_messages = messages.query.filter(messages.room_id == id).all(),id=id,name = room.query.get(id).room_name)

@app.template_filter('formatdatetime')
def format_datetime(value, format="%I:%M %p %d %b %Y"):
    if value is None:
        return ""
    return value.strftime(format)

if __name__ == '__main__':
    app.run()

