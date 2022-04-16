from flask import Flask, render_template, request, redirect, url_for
from forms import sign_up_form_class, sign_in_form_class, new_room_class, send_message_class,go_to_room_class


app = Flask(__name__)
app.config["SECRET_KEY"] = "whatever123"


@app.route('/', methods=["GET", "POST"])
def main():  # put application's code here
    return render_template('home.html')


@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    sign_up_form_obj = sign_up_form_class()
    if sign_up_form_obj.validate_on_submit():
        pass
    else:
        pass
    return render_template('sign_up.html', sign_up_form=sign_up_form_obj)


@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    sign_in_form_obj = sign_in_form_class()
    if sign_in_form_obj.validate_on_submit():
        pass
    else:
        pass
    return render_template('sign_in.html', sign_in_form=sign_in_form_obj)

@app.route('/create_room', methods = ["GET", "POST"])
def create_room():
    create_room_form_obj = new_room_class()
    if create_room_form_obj.validate_on_submit():
        pass
    else:
        pass
    return render_template('create_room.html', create_room_form=create_room_form_obj)

@app.route('/go_to_room', methods = ["GET", "POST"])
def go_to_room():
    go_to_room_form_obj = go_to_room_class()
    if go_to_room_form_obj.validate_on_submit():
        pass
    else:
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
