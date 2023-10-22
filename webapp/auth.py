from flask import Blueprint, request, flash, render_template, redirect, url_for, session
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.database import User
import re
from webapp import db, oauth
import secrets

auth = Blueprint('auth', __name__)
re_email = re.compile(r'^([a-zA-Z0-9\\_\\-\\.]+)@([a-zA-Z]+).(.+)$')
re_password = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[?!@#$%^&*-+]).{8,}$')

def generate_random_string(length=32):
    return secrets.token_urlsafe(length)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)

@auth.route("/google-login")
def googleLogin():
    redirect_uri = url_for("auth.callback", _external=True)

    # Generate a random state and nonce and store them in the session
    state = generate_random_string()
    nonce = generate_random_string()
    session['oauth_state'] = state
    session['oauth_nonce'] = nonce

    # Include state and nonce in the OAuth authorization request
    google_oauth = oauth.scanapp.authorize_redirect(redirect_uri, state=state, nonce=nonce)

    return google_oauth

@auth.route("/callback")
def callback():
    # Retrieve the OAuth state and nonce from the session
    state = session.pop('oauth_state', None)
    nonce = session.pop('oauth_nonce', None)
    if state is None or nonce is None:
        flash('OAuth state or nonce is missing.', category='error')
        return redirect(url_for('auth.login'))

    # Fetch the OAuth token
    token = oauth.scanapp.authorize_access_token()
    try:
        user_info = oauth.scanapp.parse_id_token(token, nonce=nonce)
        email = user_info['email']

        # Check if the user already exists in your database
        user = User.query.filter_by(email=email).first()

        if user is None:
            user = User(email=email, username=email)
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash('Login successful!', category='success')

    except Exception as e:
        flash(f'Error parsing ID token: {str(e)}', category='error')

    return redirect(url_for("views.home"))



@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method =='POST':
        username = request.form.get('username')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        birthday = request.form.get('birthday')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')


        # Conditions for email registration
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email has already been used for an account.', category='error')
        elif not re.fullmatch(re_email, email):
            flash('Email does not meet requirements', category='error')            
        elif not re.fullmatch(re_password, password):
            flash('Password should contain at least 8 characters, one uppercase, one lowercase, one number, and one special character (?!@#$%^&*-+).', category='error')
        elif password2 != password:
            flash('Password does not match.', category ='error')
        else:
            # Create new user account and add to the database
            new_user = User(
            username=username, 
            firstName=firstName, 
            lastName=lastName, 
            birthday=birthday, 
            email=email, 
            password=generate_password_hash(password, method='sha256')
            )

            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')

            return redirect(url_for('auth.login'))

    return render_template("register.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

