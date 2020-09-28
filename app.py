import click
from flask import escape, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
import os
import sys
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class User(db.Model):
    """docstring for ClassName"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialize Database.')


@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)


@app.route('/index')
@app.route('/home')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'


@app.route('/user/<name>')
def user_page(name):
    return "User: %s" % escape(name)


@app.route('/test')
def test_url_for():
    # 下面是调用试例
    print(url_for('hello'))
    print(url_for('user_page', name="criss"))
    print(url_for('user_page', name="alice"))
    print(url_for('user_page', name="bob"))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return "Test Page"


@app.cli.command()
def forge():
    """生成假数据"""
    db.create_all()
    name = 'Nathon Drake'
    movies = [
        # {'title':'Forist Gump', 'year':'1991'}
        {'title': 'Iron Man', 'year': '2008'},
        {'title': 'Incredible Hulk', 'year': '2008'},
        {'title': 'Captain America', 'year': '2008'},
        {'title': 'Thor', 'year': '2010'},
        {'title': 'Avengers', 'year': '2012'},
        {'title': 'Captain America:Cival War', 'year': '2015'},
        {'title': 'Blank Panther', 'year': '2017'},
        {'title': 'Avengers:Infinity War', 'year': '2018'},
        {'title': 'Captain Marvel', 'year': '2019'},
        {'title': 'Avengers:End Game', 'year': '2019'}
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done!')
