from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash , check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      email = request.form.get('email')
      password = request.form.get('password')


      user = User.query.filter_by(email=email).first()
      if user and check_password_hash(user.password, password):
         login_user(user)
         flash('Logged in successfully', 'success')
         return redirect(url_for('views.home'))
      else:
        flash('Invalid email or password', category='error')


   return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
   logout_user()
   flash('Logged out', 'info')
   return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists.', category='error')
            return redirect(url_for('auth.sign_up'))

        if password1 != password2:
            flash('Passwords do not match', 'danger')
        elif len(password1) < 6:
            flash('Password must be 6+ characters', 'danger')
        else:
            new_user = User(
                name=name,
                email=email,
                password=generate_password_hash(password1)
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Please login.', 'success')
            return redirect(url_for('auth.login'))

    #  Always return a page for GET requests (and if POST fails validation)
    return render_template('sign_up.html', user=current_user)