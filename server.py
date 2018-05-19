from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
from os import environ
import gork
from gorkdata import User
import gunicorn
import forms
from uuid import uuid4
from pprint import pprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dsafjewoijfc09c32u89cn34t89j4u3r98vnfh4n3v284h9fvojer9gnv034v'
csrf = CSRFProtect(app)

# LOGIN

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)

print("IM RUNNING!==============================")

# ROUTES
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game')
@login_required
def game():
    return render_template('game.html', username=current_user.name, ssl=('DATABASE_URL' in environ))


@app.route('/geotest')
def geotest():
    return render_template('geotest.html')


@app.route('/scan',methods=['POST'])
@login_required
@csrf.exempt
def scan():
    form = forms.PosForm()
    if form.validate_on_submit():
        my_coords = form.pos()
        acc = form.acc.data
        return jsonify({'things': gork.look_around(my_coords)})
    else:
        return jsonify({'error':form.errors})


@app.route('/dig', methods=['POST'])
@login_required
@csrf.exempt
def dig():
    form = forms.PosForm()
    if form.validate_on_submit():
        return jsonify(gork.dig_at(form.pos(),current_user))
    else: return jsonify({'error':form.errors})


@app.route('/register',methods=['GET','POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        new_user = User.register(
                name=form.username.data,
                email=form.email.data,
                pw=form.password.data
                )
        login_user(new_user)
        return redirect(url_for('game'))
    else:
        if (form.is_submitted()):
            pprint(form.errors)
        return render_template('register.html', form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        if form.authenticated():
            login_user(User.get_by_name(form.username.data))
            return redirect(url_for('game'))
        else:
            return "Nah, man.\n" #TODO display error instead
    else:
        if (form.is_submitted()):
            print(form.errors)
        return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=7001)
