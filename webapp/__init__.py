from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
oauth = OAuth()
DB_NAME= "basescanner.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1wri039fizmxvne93iclskhifhwklrgn'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Initialize OAuth for Google Login
    oauth.init_app(app)
    oauth.register(
        name="scanapp",
        client_id="905455343017-a9hgjar8lghiekip54rhd7191e1ppem3.apps.googleusercontent.com",
        client_secret="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",
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        authorize_params=None,
        authorize_response=None,
        authorize_token_url="https://accounts.google.com/o/oauth2/token",
        token_endpoint="https://accounts.google.com/o/oauth2/token",
        userinfo_endpoint="https://www.googleapis.com/oauth2/v1/userinfo",
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
        client_kwargs={'scope': 'openid email profile'},
    )

    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    # importing blueprints
    from webapp.views import views
    from webapp.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

 
    from webapp.database import User
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app


# create a new database if it does not exist
def create_database(app):
    if not path.exists('webapp/' + DB_NAME):
        db.create_all(app=app)
        print('Database Created!')

