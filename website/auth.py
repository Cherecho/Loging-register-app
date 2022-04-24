from flask import Blueprint, render_template, flash, request, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth' , __name__)


@auth.route('/login' , methods=['get' , 'post'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('pswd')

        user = User.query.filter_by(name=name).first()
        if user:
            if check_password_hash(user.password , password):
                flash('Logged in successfully!' , category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.' , category='error')
        else:
            flash('Username does not exist.' , category='error')
    return render_template("login.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sing-up' , methods=['GET' , 'POST'])
def sing_up():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        pswd1 = request.form.get('pswd')
        pswd2 = request.form.get('pswd2')

        user = User.query.filter_by(name=name).first()
        if user:
            flash('Username already registered.' , category='error')
        elif len(name) < 4:
            flash('Username must be greater than 3 characters.' , category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 character.' , category='error')
        elif pswd1 != pswd2:
            flash('Passwords don\'t match.' , category='error')
        elif len(pswd1) < 7:
            flash('Password must be at least 7 characters.' , category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(pswd1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Acount Created!', category='success')
            return redirect(url_for('views.home'))
        print(name)

    return render_template("sing_up.html")