from flask import Flask, render_template, request
from forms import sign_up_form_class


app = Flask(__name__)
app.config["SECRET_KEY"] = "whatever123"


@app.route('/', methods=["GET", "POST"])
def main():  # put application's code here
    return render_template('main.html', name='Hello Sravanth')


@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    sign_up_form_obj = sign_up_form_class()
    if sign_up_form_obj.validate_on_submit():
        pass
    else:
        pass
    return render_template('sign_up.html', sign_up_form=sign_up_form_obj,)



if __name__ == '__main__':
    app.run()
