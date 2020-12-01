import os
import sys

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_babelex import Babel

# from watchlist.models import User

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app = Flask(__name__)
app.secret_key = 'secret string'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name="FlaskAdmin", template_mode="bootstrap3")
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(app.root_path, os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'   # 中文国际化
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'   # 中文国际化
# app.config['STATICFILES_DIRS'] = os.path.join(app.root_path, 'static')
babel = Babel(app)


@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user


@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)


from watchlist import views, errors, commands, admin_view, forms  # noqa: E402, E501, F401
