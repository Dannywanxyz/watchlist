from flask import render_template
from watchlist import app
from watchlist.models import User


@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('errors/404.html', user=user), 404


@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
