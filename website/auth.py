from flask import Blueprint, render_template, request, flash, redirect, url_for

from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Wrong password, try again', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logoutPage():
    logout_user()
    return redirect(url_for('auth.login_page'))


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match. ', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)



"""
@auth.route('/Admin')
def admin():
    if request.method == 'POST':
        username = request.form.get('user_name')
        email = request.form.get('email')

        admin = Administrator.query.filter_by(email=email).first()
        if admin:
            if username:
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.admin_dashboard'))
            else:
                flash('Wrong username, try again', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template("admin/Admin.html", user=current_user)



@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form.get('user_name')
        email = request.form.get('email')
        password = request.form.get('password')

        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(username) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password is None or len(password) < 5:
            flash('Password must be greater than 5 characters.', category='error')
        else:
            new_admin = Administrator(email=email,
                            user_name=username,
                            password=generate_password_hash(password, method='pbkdf2_sha256'))
            db.session.add(new_admin)
            db.session.commit()
            flash('Account Registered', category='success')
            return redirect(url_for('views.admin_dashboard'))
    return render_template('admin/register.html')

"""