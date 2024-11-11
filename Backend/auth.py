'''Manages the authentication system'''
from flask_login import login_user, logout_user, login_required, current_user
from flask import redirect, url_for, render_template, request, Blueprint, flash
from . import db, login_manager
from . models import User

auth = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''Handles logging in user'''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)  # flask handles log in of user
            return redirect(url_for('views.home'))
        else:
            return 'Invalid Login'
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    '''Tells flask user has logged out'''
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    '''Handles signing up user'''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('User already exists')
            return redirect(url_for('auth.signup'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        # after adding user to db, log them in
        login_user(new_user)
        flash('User created')
        return redirect(url_for('views.home'))
    return render_template('signup.html')
