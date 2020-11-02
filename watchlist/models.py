from flask_login import UserMixin
from watchlist import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


class User(db.Model, UserMixin):
    """docstring for ClassName"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))  # 密码散列

    def set_password(self, password):  # 设置密码方法，接收密码作为参数
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):  # 验证密码方法， 接收密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值


class Movie(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    content = db.Column(db.Text, nullable=False)
    tag = db.Column(db.String(64), nullable=True)
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now)

    def __repr__(self):
        return '<User %r>' % self.title
