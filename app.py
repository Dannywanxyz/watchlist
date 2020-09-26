from flask import escape, url_for
from flask import Flask, render_template
app = Flask(__name__)
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


@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)


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
