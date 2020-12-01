from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from watchlist import app, db
from watchlist.models import Movie, User, Article
from watchlist.forms import LoginForm


@app.route('/', methods=['GET', 'POST'])
def index():
    movies = Movie.query.all()
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
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


@app.route('/movie/detail/<int:movie_id>', methods=['GET'])
# @login_required
def detail(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        flash('电影记录不存在！')
        return redirect(url_for('index'))
    print(movie_id)
    movie_article = Article.query.get(movie_id)
    if not movie_article:
        flash('没有此电影的文章。')
        return redirect(url_for('index'))

    return render_template('detail.html', movie_article=movie_article)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        # print(password)
        if not username or not password:
            flash('Invalid input!')
            return redirect(url_for('login'))

        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login Success!')
            return redirect(url_for('index'))

        flash('Invalid username or password')
        return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input')
            return redirect(url_for('settings'))

        current_user.name = name
        db.session.commit()
        flash('Settings Updated!')
        return redirect(url_for('index'))

    return render_template('settings.html')
