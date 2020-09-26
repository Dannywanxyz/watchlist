from flask import escape, url_for
from flask import Flask
app = Flask(__name__)


@app.route('/')
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
    print(url_for('user_page', name="david"))
    print(url_for('user_page', name="alice"))
    print(url_for('user_page', name="bob"))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return "Test Page"
