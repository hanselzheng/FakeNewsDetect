from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from webapp.machine import predict_news

views = Blueprint('views', __name__)

# Home Page
@views.route('/', methods=['GET'])
def home():
    user = None

    if current_user.is_authenticated:
        user = current_user

    return render_template('home.html', user=user)

# Detection Page
@views.route('/fact-checker', methods=['GET', 'POST'])
@login_required
def fact_check():
    prediction_label = None

    if request.method == 'POST':
        article = request.form.get("article")

        # Calling machine function to predict user input
        prediction_label = predict_news(article)

        if prediction_label == 0:
            flash('This news is reliable!', category='success')
        else:
            flash('This news is unreliable!', category='error')


    return render_template('factcheck.html', user=current_user, prediction_result=prediction_label)


# About Us Page
@views.route('/about')
def about():
    user = None

    if current_user.is_authenticated:
        user = current_user

    return render_template('about.html', user=user)

