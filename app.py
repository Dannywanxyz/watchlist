import os
import sys

import click
from flask import (Flask, escape, flash, redirect, render_template, request,
                   url_for)
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'
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


# @app.route('/index')


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
    # print()
    print(url_for('user_page', name="alice"))
    print(url_for('user_page', name="bob"))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return "Test Page"


# @app.cli.command()
# def forge():
#     """生成假数据"""
#     db.create_all()
#     name = 'Nathon Drake'
#     movies = [
#         # {'title':'Forist Gump', 'year':'1991'}
#         {'title': 'Iron Man', 'year': '2008'},
#         {'title': 'Incredible Hulk', 'year': '2008'},
#         {'title': 'Captain America', 'year': '2008'},
#         {'title': 'Thor', 'year': '2010'},
#         {'title': 'Avengers', 'year': '2012'},
#         {'title': 'Captain America:Cival War', 'year': '2015'},
#         {'title': 'Blank Panther', 'year': '2017'},
#         {'title': 'Avengers:Infinity War', 'year': '2018'},
#         {'title': 'Captain Marvel', 'year': '2019'},
#         {'title': 'Avengers:End Game', 'year': '2019'}
#     ]
#     user = User(name=name)
#     db.session.add(user)
#     for m in movies:
#         movie = Movie(title=m['title'], year=m['year'])
#         db.session.add(movie)

#     db.session.commit()
#     click.echo('Done!')


@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html', user=user), 404


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


@app.route('/', methods=['GET', 'POST'])
def index():
    movies = Movie.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input')
            return redirect(url_for('index'))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item Created')
        return redirect(url_for('index'))

    # user = User.query.first()
    # print(inject_user())
    # return render_template('index.html', user=user, movies=movies)
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == "POST":
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input')
            return redirect(url_for('index'))
        movie.title = title
        movie.year = year
        # db.session.add(movie)
        db.session.commit()
        flash('Item Updated')
        return redirect(url_for('index'))
    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted')
    return redirect(url_for('index'))
